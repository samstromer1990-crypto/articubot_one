#!/usr/bin/env python3
import sys
import select
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

BANNER = """
-----------------------------------------------------------
     Direct-Drive Keyboard Teleop (Zero-Lag)
-----------------------------------------------------------
Controls:
    W : Drive Forward (1.2 m/s)
    S : Drive Backward (-1.2 m/s)
    A : Turn Left (2.0 rad/s)
    D : Turn Right (-2.0 rad/s)

    Space / K : Full Stop
    + / -     : Increase / Decrease speed
    Q / Ctrl-C: Quit
-----------------------------------------------------------
"""

class DirectTeleop(Node):
    def __init__(self):
        super().__init__('direct_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.lin_speed = 1.2
        self.ang_speed = 2.0

    def send_cmd(self, lin, ang):
        msg = Twist()
        msg.linear.x = float(lin)
        msg.angular.z = float(ang)
        self.pub.publish(msg)

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = DirectTeleop()
    print(BANNER)

    target_lin = 0.0
    target_ang = 0.0

    try:
        while rclpy.ok():
            key = get_key(settings)
            if key == '\x03' or key in ['q', 'Q']:
                break
            elif key in ['w', 'W']:
                target_lin = node.lin_speed
                target_ang = 0.0
                node.send_cmd(target_lin, target_ang)
                print(f"\r[DRIVING] Forward: {target_lin:+.2f} m/s                      ", end='', flush=True)
            elif key in ['s', 'S']:
                target_lin = -node.lin_speed
                target_ang = 0.0
                node.send_cmd(target_lin, target_ang)
                print(f"\r[DRIVING] Reverse: {target_lin:+.2f} m/s                      ", end='', flush=True)
            elif key in ['a', 'A']:
                target_ang = node.ang_speed
                node.send_cmd(target_lin, target_ang)
                print(f"\r[TURNING] Left: {target_ang:+.2f} rad/s                       ", end='', flush=True)
            elif key in ['d', 'D']:
                target_ang = -node.ang_speed
                node.send_cmd(target_lin, target_ang)
                print(f"\r[TURNING] Right: {target_ang:+.2f} rad/s                      ", end='', flush=True)
            elif key in [' ', 'k', 'K']:
                target_lin = 0.0
                target_ang = 0.0
                node.send_cmd(0.0, 0.0)
                print(f"\r[STOPPED]                                                      ", end='', flush=True)
            elif key == '+':
                node.lin_speed = round(node.lin_speed + 0.2, 1)
                print(f"\rSpeed set to: {node.lin_speed:.1f} m/s                         ", end='', flush=True)
            elif key == '-':
                node.lin_speed = max(0.2, round(node.lin_speed - 0.2, 1))
                print(f"\rSpeed set to: {node.lin_speed:.1f} m/s                         ", end='', flush=True)
            elif key == '':
                # Keep active motion alive to avoid topic starvation
                if target_lin != 0.0 or target_ang != 0.0:
                    node.send_cmd(target_lin, target_ang)

    except Exception as e:
        print(e)
    finally:
        node.send_cmd(0.0, 0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()
        print("\nTeleop closed.")

if __name__ == '__main__':
    main()
