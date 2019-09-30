#!/usr/bin/env python

import rospy
import sys, select, termios, tty
import geometry_msgs.msg
from geometry_msgs.msg import Point, PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers

def getKey():
  tty.setraw(sys.stdin.fileno())
  rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

  if rlist:
      key = sys.stdin.read(1)

  else:
      key = ''

  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

  return key

class DetectMarker():
 
    def __init__(self):
        rospy.init_node("sub_ar_pose")
        topic_name = 'cmd_vel'
        
        self.maker_num = 0;
        self.pose_len = 0.0
        self.pose_len_an = 0.0
        self.pub = rospy.Publisher(topic_name, geometry_msgs.msg.Twist, queue_size=5)
        

        # Read in an optional list of valid tag ids
        self.tag_ids = rospy.get_param('~tag_ids', None)
 
        # Publish the COG on the /target_pose topic as a PoseStamped message
        #self.tag_pub = rospy.Publisher("target_pose", PoseStamped, queue_size=5)
        
 
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)
 
        rospy.loginfo("Publishing combined tag COG on topic /target_pose...")
    
    def get_tags(self, msg):
        # Initialize the COG as a PoseStamped message
        p = PoseStamped()
 
        # Get the number of markers
        n = len(msg.markers)
 
        t = geometry_msgs.msg.Twist()
        t.linear.x  = t.linear.y  = t.linear.z  = 0.0
        t.angular.x = t.angular.y = t.angular.z = 0.0
 
        # If no markers detected, just return
        if n == 0:
            return
 
        # Iterate through the tags and sum the x, y and z coordinates            
        for tag in msg.markers:
             
            # Skip any tags that are not in our list
            if self.tag_ids is not None and not tag.id in self.tag_ids:
                continue
 
            rospy.loginfo("------------- id ---------------------------")
            rospy.loginfo("  id = %d"%(tag.id))
             
            # Sum up the x, y and z position coordinates of all tags
            p.pose.position.x = tag.pose.pose.position.x
            p.pose.position.y = tag.pose.pose.position.y
            p.pose.position.z = tag.pose.pose.position.z
            self.pose_len = p.pose.position.z
            self.pose_len_an = p.pose.position.x 
            if(tag.id == 2): 
               if(self.pose_len_an > 0.25):
                  t.angular.z = -0.01
               elif(self.pose_len_an < 0.0):
                  t.angular.z = 0.01
               else:
                  t.angular.z = 0.00
                  if(self.pose_len > 0.8):
                     t.linear.x = 0.01
                  if(self.pose_len < 0.8):
                     t.linear.x = 0.0
            self.pub.publish(t)
            #p.pose.orientation.x = tag.pose.pose.orientation.x
            #p.pose.orientation.y = tag.pose.pose.orientation.y
            #p.pose.orientation.z = tag.pose.pose.orientation.z
            #p.pose.orientation.w = tag.pose.pose.orientation.w
 
            rospy.loginfo("------------- positions -------------------")
            rospy.loginfo("  px = %f"%(p.pose.position.x))
            rospy.loginfo("  py = %f"%(p.pose.position.y))
            rospy.loginfo("  pz = %f"%(p.pose.position.z))
 
            #rospy.loginfo("------------- orientaions -----------------")
            #rospy.loginfo("  ox = %f"%(p.pose.orientation.x))
            #rospy.loginfo("  oy = %f"%(p.pose.orientation.y))
            #rospy.loginfo("  oz = %f"%(p.pose.orientation.z))
            #rospy.loginfo("  ow = %f"%(p.pose.orientation.w))

            # Give the tag a unit orientation
            #p.pose.orientation.w = 1
 
            # Add a time stamp and frame_id
            #p.header.stamp = rospy.Time.now()
            #p.header.frame_id = msg.markers[0].header.frame_id
 
            # Publish the COG
            #self.tag_pub.publish(p)      
   
if __name__ == '__main__':

    try:
        DetectMarker()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AR Tag Tracker node terminated.")
       
 
    
     
