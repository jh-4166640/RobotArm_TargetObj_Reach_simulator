#import ErrorDoc as ERd

class RobotStatus():
    link_number=4 #link의 갯수
    joint_number=6 #joint의 갯수
    link_length=() #link 각각의 길이
    effector_type="" #end-effector 종류
    effector_length = 0
    motor_angle_range = () 
    temp_angle_range = [0,0,0,0,0,0] #튜플에 저장하기 위한 임시 저장용 리스트
    count_set_angle = 0 #몇번 세팅 되었는지 카운트
    set_angle_motornumber=[] #세팅된 번호 저장
    
    
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
            self.link_length += tuple(llen)
    
    def RegisterEndEffector(self,eftype,eflen):
        """
        End-Effector type and length register

        Args:
            eftype (String): effector type
            eflen (int): effector lenght
        """
        self.effector_type = eftype
        self.effector_length = eflen
    
    def set_AngleRange(self, idx, _start, _stop): #Servo motor의 기준각도~최대각도 지정
        """
        Each Servo Motor rotate angle setting function

        Args:
            idx (int): servo motor angle index
            _start (int): min angle -180~179
            _stop (int): max angle -179~180
        """
        if idx >= self.joint_number:
            pass
            # OutOfBound index error 범위 지정 오류
        elif _start >= _stop:
            pass
            # 최대 최소 범위 지정 오류
        else :
            if idx not in self.set_angle_motornumber:
                self.count_set_angle += 1
                self.set_angle_motornumber.append(idx)
            ang = (_start, _stop)
            self.temp_angle_range[idx]=ang
            if self.count_set_angle == self.joint_number:
                self.motor_angle_range += tuple(self.temp_angle_range)
        
