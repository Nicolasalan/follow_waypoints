#! /usr/bin/env python3

from robot_nav.save_waypoints import SaveWaypoints
import unittest


class CaseA(unittest.TestCase):

    def setUp(self):
        self.rc = SaveWaypoints()

    def test_euler_quaternion(self):

        qx, qy, qz, qw = self.angles(-0.486865, 6.297588, 0)
        self.assertEquals(qx, 0.2410290872214269, "0.2410290872214269!=0.2410290872214269")
        self.rc.shutdownhook()

class CaseB(unittest.TestCase):
     
    def setUp(self):
        self.rc = SaveWaypoints()

    def test_path_waypoints(self):

        data = self.rc.yaml_loader('/social_ws/src/waypoints/way.yaml')
        self.assertTrue(data, "integration failure, not found path waypoints")
        self.rc.shutdownhook()


class TestSuite(unittest.TestSuite):
    def __init__(self):
        super(TestSuite, self).__init__()
        self.addTest(CaseA())
        self.addTest(CaseB())