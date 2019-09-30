#!/usr/bin/env python
 
# To use rospy modules
import rospy
 
# For twist message
import geometry_msgs.msg
 
from mylib.GetChar import Getchar
from mylib.Bong import Bong
 
BURGER_MAX_LIN_VEL = 0.22
BURGER_MIN_LIN_VEL = -0.22
BURGER_MAX_ANG_VEL = 2.84
BURGER_MIN_ANG_VEL = -2.84
 
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1
 
msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x
 
w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)
 
space key, s : force stop
 
CTRL-C to quit
"""

if __name__ == '__main__':
 
    
    #########################
    # Initialisation
    #########################
    # Initialises ros node. Mostlsy, first line command for ros python executable
    rospy.init_node('command_turtle')
 
    # Twist message publisher. (Topic name, Topic Type, Queue Size)
    # Turtlesim topic name
    #topic_name = 'turtle1/cmd_vel'
    topic_name = 'cmd_vel'
 
    # Kobuki Topic name
    # topic_name = '/mobile_base/commands/velocity'
 
    # Turtlebot3 Topic name
    # topic_name = ''
 
    pub = rospy.Publisher(topic_name, geometry_msgs.msg.Twist, queue_size=5)
    # Give a graceful time to setup publisher 
    rospy.sleep(1.0)
    rospy.loginfo("Initilsed")
   
    kb = Getchar()
    bo = Bong()
    # Instantiate Twist Message to publish
    t = geometry_msgs.msg.Twist()
 
    t.linear.x = 0.0
    t.linear.y = 0.0
    t.linear.z = 0.0
    t.angular.x = 0.0
    t.angular.y = 0.0
    t.angular.z = 0.0

 
    status = 0
 
    # Time elapse
    duration = 0.1 # in seconds
    ros_duration = rospy.Duration(duration) # in ros time
    current = rospy.Time.now() # Current ros time
    ends = current + ros_duration 
 
    # Log message
    rospy.loginfo("Publishing Twist message to %s for %s seconds"%(topic_name, duration))
     
    try:
        print msg
 
        while not rospy.is_shutdown():
            # Publish Twist message
            key = kb.getch()
 
            if key == 'w':      #################################################################
                if t.linear.x <= BURGER_MAX_LIN_VEL - LIN_VEL_STEP_SIZE :
                    t.linear.x = t.linear.x + LIN_VEL_STEP_SIZE
                else :
                    t.linear.x = BURGER_MAX_LIN_VEL
 
                status = status + 1
 
                print("linear velocity = %f,  angular velocity = %f"%(t.linear.x, t.angular.z))
 
            elif key == 'x' :   #################################################################
                if t.linear.x >= BURGER_MIN_LIN_VEL + LIN_VEL_STEP_SIZE :
                    t.linear.x = t.linear.x - LIN_VEL_STEP_SIZE
                else :
                    t.linear.x = BURGER_MIN_LIN_VEL
 
                status = status + 1
 
                print("linear velocity = %f,  angular velocity = %f"%(t.linear.x, t.angular.z))
 
            elif key == 'a' :   #################################################################
                if t.angular.z <= BURGER_MAX_ANG_VEL - ANG_VEL_STEP_SIZE :
                    t.angular.z = t.angular.z + ANG_VEL_STEP_SIZE
                else :
                    t.angular.z = BURGER_MAX_ANG_VEL
 
                status = status + 1
 
                print("linear velocity = %f,  angular velocity = %f"%(t.linear.x, t.angular.z))
 
            elif key == 'd' :   #################################################################
                if t.angular.z >= BURGER_MIN_ANG_VEL + ANG_VEL_STEP_SIZE :
                    t.angular.z = t.angular.z - ANG_VEL_STEP_SIZE
                else :
                    t.angular.z = BURGER_MIN_ANG_VEL
 
                status = status + 1
 
                print("linear velocity = %f,  angular velocity = %f"%(t.linear.x, t.angular.z))
 
            elif key == ' ' or key == 's' : ###################################################
                t.linear.x  = 0.0
                t.angular.z = 0.0
 
                status = status + 1
 
                print("linear velocity = %f,  angular velocity = %f"%(t.linear.x, t.angular.z))
 
            if bo.count == 20 :
                print Msg
                
 
            #twist = geometry_msgs.msg.Twist()
 
            pub.publish(t)
 
            rospy.sleep(0.01)
                     
 
    except KeyboardInterrupt:
        rospy.loginfo("Program ends.")
