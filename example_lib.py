#!/usr/bin/env python


import rospy
import geometry_msgs.msg
from mylib.GetChar import *
from mylib.Bong import *
mag = '''
           w
        a  s  d
        'q' ' '(space) : to stop
        'w'            : forward
        's'            : forward
        '+'            : speedup
        '-'            : speeddown
        'a'            : ccw(+)
        'd'            : cw(+)
        'c'            : circle
        'p'            : square
'''

#def speed_up_down(ch, speed):    
#   if ch == '+':
#      if(speed < Turtle_speed_MAX):
#         speed = speed + 0.01
#         return speed
#   elif ch == '-':
#      if(speed > Turtle_speed_MIN):
#         speed = speed - 0.01
#         return speed
#   else:
#      return speed
   
if __name__ == '__main__':

  ch = ''
  speed = 0.0
  an_speed = 0.0
  Turtle_speed_MAX = 0.22
  Turtle_speed_MIN = 0
  Turtle_angle_MAX = 2.22
  Turtle_angle_MIN = 0
  #########################
  # Initialisation
  #########################
  # Initialises ros node. Mostlsy, first line command for ros python executable
  rospy.init_node('command_turtle')
  topic_name = 'turtle1/cmd_vel'   # for 'turtlesim_nod'
  #topic_name = 'cmd_vel'   
  
  # Kobuki Topic name
  # topic_name = '/mobile_base/commands/velocity'

  pub = rospy.Publisher(topic_name, geometry_msgs.msg.Twist, queue_size=5)
  # Give a graceful time to setup publisher 
  rospy.sleep(1.0)
  rospy.loginfo("Initialsed")

  # Instantiate Twist Message to publish
  t = geometry_msgs.msg.Twist()

  # Time elapse
  '''
  duration = 5.0 # in seconds
  ros_duration = rospy.Duration(duration) # in ros time
  current = rospy.Time.now() # Current ros time
  ends = current + ros_duration
  '''
  # Log message
  rospy.loginfo("Publishing Twist message")# to %s for %s seconds"%(topic_name, duration))
  t.linear.x  = t.linear.y  = t.linear.z  = 0.0
  t.angular.x = t.angular.y = t.angular.z = 0.0
  
  a = GetChar()
  b = Bong()
  
  while not rospy.is_shutdown():
  
    while ch != 'Q':
  
      
      ch = a.getch()
      #speed = speed_up_down(ch, speed)
      (speed, an_speed,t) = move_turtle(ch,speed,an_speed,t)
      
      if ch == 'c':
        getcircle() 
      elif ch == 'p':
        getsqaure()
      else:
        pass
      
      # Publish Twist message
      pub.publish(t)
      '''
      if rospy.Time.now() > ends:
      t.linear.x  = t.linear.y  = t.linear.z  = 0.0
      t.angular.x = t.angular.y = t.angular.z = 0.0
      pub.publish(t)
      ''' 

    break
    #rospy.loginfo("Program ends.")
