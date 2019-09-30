#! /usr/bin/env python

import os
import time
import sys
import termios
import atexit
import tty
from select import select
 
# class for checking keyboard input
class GetChar:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
 
        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
 
        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)
     
     
    def set_normal_term(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
 
    def getch(self):        # get 1 byte from stdin
        """ Returns a keyboard character after getch() has been called """
        return sys.stdin.read(1)
 
    def chk_stdin(self):    # check keyboard input
        """ Returns True if keyboard character was hit, False otherwise. """
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr
 
def getKey():
  tty.setraw(sys.stdin.fileno())
  rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

  if rlist:
      key = sys.stdin.read(1)

  else:
      key = ''

  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

  return key

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
      
def move_turtle(ch,speed,an_speed,t): 
      Turtle_speed_MAX = 2.2
      Turtle_angle_MAX = 2.2   
      Turtle_speed_MIN = 0
      Turtle_angle_MIN = -2.2           
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
         if(an_speed < 0):
            an_speed = 0.1
         if(an_speed < Turtle_angle_MAX):
            an_speed = an_speed + 0.1
         t.linear.x  = 0.0
         t.angular.z = an_speed 
      elif ch == 'd':
         if(an_speed > 0):
            an_speed = -0.1
         if(an_speed > Turtle_angle_MIN):
            an_speed = an_speed - 0.1
         t.linear.x  =  0.0
         t.angular.z = an_speed 
      elif ch == 'q' or ch == ' ':
         t.linear.x = 0.0
         t.angular.z = 0.0
      else:
         pass
      return (speed, an_speed,t)

 
 
