import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import threading
import time
from rclpy import Parameter
from rcl_interfaces.msg import SetParametersResult

class RotateWheelNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("start")
        self.joint_states_publisher=self.create_publisher(JointState,"joint_states",10)
        self.declare_parameter("left_wheel_speed",0.0)
        self.declare_parameter("right_wheel_speed",0.0)
        self.left_speed = self.get_parameter("left_wheel_speed").value
        self.right_speed = self.get_parameter("right_wheel_speed").value
        self.add_on_set_parameters_callback(self.param_callback)
        #initialize
        self.__init_joint_states()
        self.pub_rate=self.create_rate(30)
        #创建线程
        self.thread_=threading.Thread(target=self._thread_pub) #把函数 _thread_pub交给线程去运行
        self.thread_.start()

    def __init_joint_states(self):
        self.joint_speeds=[0.0,0.0]
        self.joint_states=JointState()
        self.joint_states.header.stamp=self.get_clock().now().to_msg()
        self.joint_states.header.frame_id=""
       
        #joint name
        self.joint_states.name=['left_wheel_joint','right_wheel_joint']
        #joint position
        self.joint_states.position=[0.0,0.0]
        #joint rate
        self.joint_states.velocity=self.joint_speeds
        self.joint_states.effort=[]

    def param_callback(self,params:list[Parameter]):
        result=SetParametersResult()
        result.successful=True
        for param in params:
            if param.name=="left_wheel_speed":
                self.left_speed=param.value
            elif param.name=="right_wheel_speed":
                self.right_speed=param.value
        self.joint_speeds=[self.left_speed,self.right_speed]     
        return result   

    def update_speed(self,speed):
        self.joint_speeds=speed

    def _thread_pub(self):
        last_update_time = time.time()   
        while rclpy.ok():
            delta_time =time.time()-last_update_time
            last_update_time=time.time()
            self.joint_states.position[0]+=delta_time*self.joint_states.velocity[0]
            self.joint_states.position[1]+=delta_time*self.joint_states.velocity[1]
            self.joint_states.velocity=self.joint_speeds
            self.joint_states.header.stamp=self.get_clock().now().to_msg()
            self.joint_states_publisher.publish(self.joint_states)
            self.pub_rate.sleep() #控制30Hz发布频率

def main(args=None):
    rclpy.init(args=args)
    node =  RotateWheelNode("rotate_yezibot_wheel")
    rclpy.spin(node)
    rclpy.shutdown()    