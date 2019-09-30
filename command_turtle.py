#!/usr/bin/env python

# To use rospy modules
import rospy

# For twist message
import geometry_msgs.msg

if __name__ == '__main__':

    #########################
    # Initialisation
    #########################
    # Initialises ros node. Mostlsy, first line command for ros python executable
    rospy.init_node('command_turtle')

    # Twist message publisher. (Topic name, Topic Type, Queue Size)
    # Turtlesim topic name
    topic_name = 'turtle1/cmd_vel'

    # Kobuki Topic name
    # topic_name = '/mobile_base/commands/velocity'

    pub = rospy.Publisher(topic_name, geometry_msgs.msg.Twist, queue_size=5)
    # Give a graceful time to setup publisher 
    rospy.sleep(1.0)
    rospy.loginfo("Initilsed")

    # Instantiate Twist Message to publish
    t = geometry_msgs.msg.Twist()
    t.linear.x = 0.5 # Controls Linear speed
    t.linear.y = 0.0
    t.linear.z = 0.0
    t.angular.x = 0.0
    t.angular.y = 0.0
    t.angular.z = 0.5 # Controls angular speed

    # Time elapse
    duration = 5.0 # in seconds
    ros_duration = rospy.Duration(duration) # in ros time
    current = rospy.Time.now() # Current ros time
    ends = current + ros_duration 

    # Log message
    rospy.loginfo("Publishing Twist message to %s for %s seconds"%(topic_name, duration))
    while not rospy.is_shutdown():
        # Publish Twist message
        pub.publish(t)
        rospy.sleep(0.1)

        if rospy.Time.now() > ends:
          break

    rospy.loginfo("Program ends.")
