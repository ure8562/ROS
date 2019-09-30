#!/usr/bin/env python

import time
import rospy
import geometry_msgs.msg
import sys, select, termios, tty
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
def getcircle():                 
   t.linear.x  = speed
   t.linear.y  = t.linear.z  = 0.0
   t.angular.x = t.angular.y = 0.0
   t.angular.z = speed * 2
   
def getsqaure():                 
   for i in range (4):
      t.linear.x = 0
      t.angular.z = 1.5708
      pub.publish(t)
      time.sleep(1)
      t.linear.x = speed
      t.angular.z = 0
      pub.publish(t)
      time.sleep(1)
      
def move_turtle(ch,speed,an_speed):            
      if   ch == 'w':
         if(speed < Turtle_speed_MAX):
            speed = speed + 0.01
         t.linear.x  = speed
         t.angular.z = 0.0
      elif ch == 's':
         if(speed > Turtle_speed_MIN):
            speed = speed - 0.01
         t.linear.x  = speed
         t.angular.z = 0.0
      elif ch == 'a':
         if(an_speed < Turtle_angle_MAX):
            an_speed = an_speed + 0.1
         t.linear.x  = 0.0
         t.angular.z = an_speed 
      elif ch == 'd':
         if(an_speed > Turtle_angle_MIN):
            an_speed = an_speed - 0.1
         t.linear.x  =  0.0
         t.angular.z = an_speed 
      elif ch == 'q' or ch == ' ':
         t.linear.x = 0.0
         t.angular.z = 0.0
      else:
         pass
      return (speed, an_speed)

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
  #topic_name = 'turtle1/cmd_vel'   # for 'turtlesim_nod'
  topic_name = 'cmd_vel'   
  
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
  while not rospy.is_shutdown():
  
    while ch != 'Q':
    
      settings = termios.tcgetattr(sys.stdin)
      
      ch = getKey()
      #speed = speed_up_down(ch, speed)
      (speed, an_speed) = move_turtle(ch,speed,an_speed)
      
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
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
      
    break

    #rospy.loginfo("Program ends.")
