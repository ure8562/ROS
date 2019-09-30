#!/usr/bin/env python

import rospy
import sys, select, termios, tty
import geometry_msgs.msg
from geometry_msgs.msg import Point, PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers


class DetectMarker():
 
    def __init__(self):
        rospy.init_node("sub_ar_pose")
        
        
        self.maker_num = 0;
        self.pose_len = 0.0
        self.pose_len_an = 0.0
        
        

        # Read in an optional list of valid tag ids
        self.tag_ids = rospy.get_param('~tag_ids', None)
 
        # Publish the COG on the /target_pose topic as a PoseStamped message
        #self.tag_pub = rospy.Publisher("target_pose", PoseStamped, queue_size=5)
        
 
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)
 
        rospy.loginfo("Publishing combined tag COG on topic /target_pose...")
    
    def get_info(self):
      return(self.pose_len, self.pose_len_an, self.maker_num)
    def get_tags(self, msg):
        # Initialize the COG as a PoseStamped message
        p = PoseStamped()
 
        # Get the number of markers
        n = len(msg.markers)
                                       
        # If no markers detected, just return
        if n == 0: 
            
            self.maker_num = 0    
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
            self.maker_num = tag.id
 
            rospy.loginfo("------------- positions -------------------")
            rospy.loginfo("  px = %f"%(p.pose.position.x))
            rospy.loginfo("  py = %f"%(p.pose.position.y))
            rospy.loginfo("  pz = %f"%(p.pose.position.z))
 
   
if __name__ == '__main__':
   topic_name = 'cmd_vel'
   pub = rospy.Publisher(topic_name, geometry_msgs.msg.Twist, queue_size=5)
   t = geometry_msgs.msg.Twist()
   t.linear.x  = t.linear.y  = t.linear.z  = 0.0
   t.angular.x = t.angular.y = t.angular.z = 0.0
   ID = 0
   len_z = 0.0
   len_x = 0.0
   
   try:
      test = DetectMarker()
      (len_z, len_x, ID) = test.get_info()
      if(ID == 0):
         rospy.loginfo("------------- finding -------------------") 
         t.angular.z = 0.1

      if(ID == 2): 
         if(len_x > 0.25):
          t.angular.z = -0.01
         elif(len_x < 0.0):
          t.angular.z = 0.01
         else:
            t.angular.z = 0.00
            if(len_z > 0.8):
               t.linear.x = 0.01
            if(len_z < 0.8):
             t.linear.x = 0.0
      pub.publish(t)   
      rospy.spin()
   except rospy.ROSInterruptException:
      rospy.loginfo("AR Tag Tracker node terminated.")
