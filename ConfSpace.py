import ErrorDoc as erd

class ConfigurationSpcae():
    _link_number=3 #link의 갯수
    _joint_number=6 #joint의 갯수
    link_length=() #link 각각의 길이 #base,bottom,mid,top,wrist,endeffect
    #effector_length = 0
    motor_angle_range = () 
    __temp_angle_range = [0,0,0,0,0,0] #튜플에 저장하기 위한 임시 저장용 리스트
    __count_set_angle = 0 #몇번 세팅 되었는지 카운트
    __set_angle_motornumber=[] #세팅된 번호 저장
    
    maxval = 0
    __offset = 0
    __target_loc = [0,0,0]
    
    def __init__(self,llen, offset):
        
        self.__count_set_angle=0
        self.__set_angle_motornumber.clear()
        self.motor_angle_range = ()
        self.link_length = ()
        
        """
        Args:
            llen (list[int]): Length of Links, list size: 5
            offset (float): step for configuration spcace create offset min offset 0.001
        """
        chk = self.RegisterLink(llen)
        if chk: # RegisterLink error
            return
        self.__offset = offset
        
    def RegisterLink(self,llen):
        """
        Link length and number register
        Args:
            _llen (list[int]): Each lenght for link
        """
        if self._link_number != len(llen):
            erd.LinkList_size_error()
            return
        else :
            self.link_length = tuple(llen)
            print(self.link_length)
    
    def set_AngleRange(self, idx, _start, _stop): #Servo motor의 기준각도~최대각도 지정
        """
        Each Servo Motor rotate angle setting function

        Args:
            idx (int): servo motor angle index
            _start (int): min angle -180~179
            _stop (int): max angle -179~180
        """
        if idx >= self._joint_number:
            erd.index_OutofRange()
            return
        else :
            if idx not in self.__set_angle_motornumber:
                self.__count_set_angle += 1
                self.__set_angle_motornumber.append(idx)
            ang = (_start, _stop)
            self.__temp_angle_range[idx]=ang
            if self.__count_set_angle == self._joint_number:
                self.motor_angle_range = tuple(self.__temp_angle_range)
                
    def setSpaceRange(self):
        for i in range(self._link_number):
            self.maxval+=self.link_length[i] 
        #self.maxval+=self.effector_length
    def setTargetLocate(self, _x, _y, _z):
        """Target object locate setting
        Args:
            _x (double): x axis value
            _y (double): y axis value
            _z (double): z axis value
        """
        self.__target_loc=[_x,_y,_z]
    def getTargetLocate(self):
        return self.__target_loc
    def getUnitOffset(self):
        return self.__offset
    #def RegisterEndEffector(self,eflen):
        #"""
        #End-Effector type and length register

        #Args:
        #    eflen (int): effector lenght
        #"""
        #self.effector_type = eftype
        #self.effector_length = eflen