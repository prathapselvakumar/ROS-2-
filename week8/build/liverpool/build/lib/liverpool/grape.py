import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class GrapeNode(Node):
    def __init__(self):
        super().__init__('grape')
        self.target_frame = 'fusion_droid'
        self.source_frame = 'robo_walker'
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                rclpy.time.Time())
            self.get_logger().info(f'{t}')
        except TransformException as ex:
            self.get_logger().info(f'Could not transform {self.target_frame} to {self.source_frame}: {ex}')

def main(args=None):
    rclpy.init(args=args)
    node = GrapeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
   
if __name__ == '__main__':
    main()
