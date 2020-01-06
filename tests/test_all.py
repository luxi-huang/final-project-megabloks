#! /usr/bin/env python

import unittest
import rospy
from sensor_msgs.msg import CameraInfo
from baxter_core_msgs.msg import EndEffectorState

class TestCases(unittest.TestCase):
    def __init__(self, *args):
        super(TestCases, self).__init__(*args)
        rospy.init_node('test_the')

    def test_tower(self):
        tower = rospy.get_param('/tower', None)
        self.assertIsNotNone(tower)

    def test_camera(self):
        self.camera_info = rospy.wait_for_message('/cameras/right_hand_camera/camera_info', CameraInfo, 3)
        self.assertEqual(self.camera_info.width, 1280)


    def test_left_gripper(self):
        #gripper = baxter_interface.Gripper('left')
        #self.assertTrue(server.calibrate_grippers(gripper))

        self.left = rospy.wait_for_message('/robot/end_effector/left_gripper/state', EndEffectorState, 3)
        self.assertEqual(self.left.calibrated, 1)

    def test_right_gripper(self):
        #gripper = baxter_interface.Gripper('right')
        #self.assertTrue(server.calibrate_grippers(gripper))

        self.right = rospy.wait_for_message('/robot/end_effector/right_gripper/state', EndEffectorState, 3)
        self.assertEqual(self.right.calibrated, 1)

if __name__=='__main__':
    import rostest
    rostest.rosrun('blocks', 'testrun', TestCases)
