#!/usr/bin/env python

import rospy
import geometry_msgs.msg
from geometry_msgs.msg import Point, PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers
  
  
def callback(msg):
  
if __name__ == '__main__':
   settings = termios.tcgetattr(sys.stdin)
   rospy.init_node("sub_ar_pose")
   topic_name = 'cmd_vel'
   
   tag_ids = rospy.get_param('~tag_ids', None)
   rospy.Subscriber("ar_pose_marker", AlvarMarkers, callback)

   rospy.loginfo("Publishing combined tag COG on topic /target_pose...")
   
   p = PoseStamped()
   if n == 0: 
      pass

   for tag in msg.markers:
            # Skip any tags that are not in our list
            if tag_ids is not None and not tag.id in tag_ids:
             continue
 
            rospy.loginfo("------------- id ---------------------------")
            rospy.loginfo("  id = %d"%(tag.id))
                     
            # Sum up the x, y and z position coordinates of all tags
            p.pose.position.x = tag.pose.pose.position.x
            p.pose.position.y = tag.pose.pose.position.y
            p.pose.position.z = tag.pose.pose.position.z

            #p.pose.orientation.x = tag.pose.pose.orientation.x
            #p.pose.orientation.y = tag.pose.pose.orientation.y
            #p.pose.orientation.z = tag.pose.pose.orientation.z
            #p.pose.orientation.w = tag.pose.pose.orientation.w
 
            rospy.loginfo("------------- positions -------------------")
            rospy.loginfo("  px = %f"%(p.pose.position.x))
            rospy.loginfo("  py = %f"%(p.pose.position.y))
            rospy.loginfo("  pz = %f"%(p.pose.position.z))


       
 
    
     
