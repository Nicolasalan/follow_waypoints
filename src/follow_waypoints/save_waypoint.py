#!/usr/bin python3

import yaml 
import rospy
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from robot_nav.srv import save_point

file_path = '/social_ws/src/waypoints/way.yaml'
class SaveWaypoint():

    def __init__(self):
        
        rospy.Service('save_waypoint', save_point, self.handler)
        rospy.loginfo('Ready to detect!')
        
    def angles(self, roll, pitch, yaw):
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return qx, qy, qz, qw
    
    def yaml_loader(self, file_path):
        try:
            with open(file_path) as f:
                return True

        except yaml.YAMLError as exc:
            return False

    def open(self):
        list_points = []
        with open(file_path) as f:
            data = yaml.safe_load(f)
            for i in data:
                list_points.append(i['position'])

        for i in list_points:
            roll_str = str(i[0]).strip('[]')
            pitch_str = str(i[1]).strip('[]')
            yaw_str = str(i[2]).strip('[]')
        
        roll, pitch, yaw = float(roll_str), float(pitch_str), float(yaw_str)

        return roll, pitch, yaw


    def save(self, name):

        name_path = '/social_ws/src/robot_data/data/map/'+name.name+'/poses.csv'
        print(name_path)
        with open(name_path, 'w') as csvfile:

            roll, pitch, yaw = self.open()
            roll_str, pitch_str, yaw_str = str(roll), str(pitch), str(yaw)
            qx, qy, qz, qw = self.angles(roll, pitch, yaw)
            csvfile.write(roll_str + ', ' + pitch_str + ', 0.0, ' + '0.0' + ', ' + str(qy) + ', ' + str(qz) + ', ' + str(qw))
            csvfile.write('\n')
            csvfile.close()
        return True

    def handler(self, request):
        num = 0
        while num == 0:
            resp = self.save(request)

            if resp is True:
                num = 1
                return "Salved!"
            else:
                num = 1
                return "Error!"

if __name__ == '__main__':
    rospy.init_node('save_waypoint', log_level=rospy.INFO)
    SaveWaypoint()

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
