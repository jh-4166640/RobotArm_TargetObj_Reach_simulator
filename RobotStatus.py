#import ErrorDoc as ERd

class RobotStatus():
    link_number=4 #link의 갯수
    joint_number=6 #joint의 갯수
    link_length=[] #link 각각의 길이
    effector_type="" #end-effector 종류
    effector_length = 0
    motor_angle_range = []
    
    
    def RegisterLink(self,llen):
        """
        Link length and number register
        Args:
            _llen (list[int]): Each lenght for link
        """
        if self.link_number != len(llen):
            pass
            #return ERd.error()
        else :
            self.link_length = llen
    
    def RegisterEndEffector(self,eftype,eflen):
        """
        End-Effector type and length register

        Args:
            eftype (String): effector type
            eflen (int): effector lenght
        """
        self.effector_type = eftype
        self.effector_length = eflen
    
    def set_AngleRange(self, idx, _start, _stop, _step): #Servo motor의 기준각도~최대각도 지정
        """
        Arm part install Servo Motor 

        Args:
            idx (int): servo motor angle index
            _start (int): basic angle
            _stop (int): limit angle
            _step (int): step size
        """
        ang = [val for val in range(_start, _stop, _step)]
        self.motor_angle_range.insert(idx,ang)