import numpy as np
import math
import ErrorDoc as erd
import time 
class RobotPose():
    dh_param = [] # theta d a alp
    
    def __init__(self, link, ang):
        self.setParam(link,ang)
    def setParam(self, link, ang):
        self.dh_param = [] # theta d a alpha
        self.dh_param.append([ang[0], 0, 0, 0]) # base
        self.dh_param.append([0, 0, 0, 90])
        self.dh_param.append([ang[1], 0, 0, 0]) # bottom
        self.dh_param.append([0, 0, link[0], 0])
        self.dh_param.append([ang[2], 0, 0, 0]) # mid
        self.dh_param.append([0, 0, link[1], 0])
        self.dh_param.append([ang[3], 0, 0, 0]) # top
        self.dh_param.append([0, 0, link[2], 0]) # EndEffector
        
    def DH_Matrix(self, th, d, a, alp):
        th = np.deg2rad(th)
        alp = np.deg2rad(alp)
        return np.array([[np.cos(th), -np.sin(th)*np.cos(alp), np.sin(th)*np.sin(alp), a*np.cos(th)],
                        [np.sin(th), np.cos(th)*np.cos(alp), -np.cos(th)*np.sin(alp), a*np.sin(th)],
                        [0, np.sin(alp), np.cos(alp), d],
                        [0, 0, 0, 1]])
    def Forward_Kinematics(self):
        T = np.eye(4)
        pos = [T[:3,3]]
        for param in self.dh_param:
            th, d, a, alp = param
            T = np.dot(T, self.DH_Matrix(th, d, a, alp))
            pos.append(T[:3, 3])
        print('pos\n',pos)
        return np.array(pos)

    def Inverse_Kinematics(self, tp, links, ang_ran):
        trg_x = tp[0]
        trg_y = tp[1]
        trg_z = tp[2]
        base = np.arctan2(trg_y, trg_x)
        r = np.sqrt(trg_x**2 + trg_y**2)
        s = trg_z - links[2]
        D = (r**2 + s**2 - links[0]**2 - links[1]**2) / (2 * links[0] * links[1])
        mid = np.arctan2(np.sqrt(1-D**2), D)
        bottom = np.arctan2(s,r) - np.arctan2(links[1] * np.sin(mid), links[0] + links[1]*np.cos(mid))
        top = 0
        base = float(np.degrees(base))
        bottom = float(np.degrees(bottom))
        mid = float(np.degrees(mid))
        top = float(np.degrees(top))
        if base < ang_ran[0][0] or base > ang_ran[0][1]:
            return False
        if bottom < ang_ran[1][0] or bottom > ang_ran[1][1]:
            return False
        if mid < ang_ran[2][0] or mid > ang_ran[2][1]:
            return False
        top_less_angle = [base,bottom,mid,top-5,0,0]
        self.setParam(links,top_less_angle)
        less_res =self.Forward_Kinematics()
        print('less res',less_res)
        top_more_angle= [base,bottom,mid,top+5,0,0]
        self.setParam(links,top_more_angle)
        more_res =self.Forward_Kinematics()
        print('more res',more_res)
        less_distance = np.sqrt((tp[0]-less_res[8][0])**2+
                                (tp[1]-less_res[8][1])**2+
                                (tp[2]-less_res[8][2])**2)
        more_distance = np.sqrt((tp[0]-more_res[8][0])**2+
                                (tp[1]-more_res[8][1])**2+
                                (tp[2]-more_res[8][2])**2)
        print('less',less_distance)
        print('more',more_distance)
        
        while True:
            if less_distance < more_distance: top-=1
            elif less_distance > more_distance: top+=1
            else:
                top=top
                break
            angles = [base,bottom,mid,top,0,0]
            self.setParam(links,angles)
            cal_res =self.Forward_Kinematics()
            cal_distance = np.sqrt((tp[0]-cal_res[8][0])**2+
                                    (tp[1]-cal_res[8][1])**2+
                                    (tp[2]-cal_res[8][2])**2)
            if cal_distance <= 0.1:
                break
        
        res_angle = [base,bottom,mid,top,0,0]
        self.setParam(links,res_angle)
        return res_angle
    def show_ROBOT_MOVEMENT(self, cur_ang, trg_ang, step):
        print('cur angle\n', cur_ang)
        print('trg angle\n', trg_ang)
        for item in trg_ang:
            if np.isnan(item) == True:
                erd.Target_OVER_ANGLE_error()
                return False
        result_angle = []
        unit_angle = []
        idx = 0
        while True:
            end_condition = True
            unit_angle.clear()
            for i in range(len(cur_ang)):
                if cur_ang[i] != trg_ang[i] or abs(cur_ang[i] - trg_ang[i]) > 0.1:
                    end_condition = False
                    if cur_ang[i] > trg_ang[i]:
                        cur_ang[i]-=step
                        if cur_ang[i] < trg_ang[i]:
                            cur_ang[i] += trg_ang[i] - cur_ang[i]
                        #cur_ang[i]=round(cur_ang[i],2)
                    elif cur_ang[i] < trg_ang[i]:
                        cur_ang[i] += step
                        if cur_ang[i] > trg_ang[i]:
                            cur_ang[i] += trg_ang[i]-cur_ang[i]
                        #cur_ang[i]=round(cur_ang[i],2)
                    unit_angle.append(cur_ang[i])
                elif cur_ang[i] == trg_ang[i] or abs(cur_ang[i] - trg_ang[i]) < 0.1:
                    unit_angle.append(cur_ang[i])
            result_angle += [unit_angle[:]]
            print('result_angle step\n', result_angle)
            if end_condition == True:
                break
        print('finally result_angle\n',result_angle)
        return result_angle