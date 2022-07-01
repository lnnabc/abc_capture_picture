#!/usr/bin/env python
from __future__ import print_function
import rospy
import time
from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Path
from sensor_msgs.msg import Image
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from capture_picture.srv import picture,pictureResponse

def handle_capture_picture(req):
    data = rospy.wait_for_message("/camera/rgb/image_raw", Image, timeout=10)
    global bridge
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
    image = image[144:336]
    now=time.localtime()
    now_time=time.strftime("%Y-%m-%d-%H-%M-%S",now)
    name = '{}'.format(now_time) 
    cv.imwrite('/home/udrive/udrive_v1_1_1/ws/image/{}.png'.format(name), image)
    print('image:  {}.png  has been saved'.format(name))
    path='/home/udrive/udrive_v1_1_1/ws/image/{}.png'.format(name) 
    return pictureResponse(path)
def capture_picture_server():
    rospy.init_node('capture_picture_server')
    s = rospy.Service('capture_picture', picture, handle_capture_picture)
    print("Ready to capture picture.")
    rospy.spin()
if __name__ == "__main__":
    bridge = CvBridge()
    capture_picture_server()