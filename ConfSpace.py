import RobotStatus as Rs

class ConfigurationSpcae(Rs.RobotStatus):
    xranges = []
    yranges = []
    zranges = []
    offset = 0.0
    target_loc = [0,0,0]
    def __init__(self):
        for i in range(0, 6):
            strs=str(self.link_length[i])
            j = 0
            places_cnt = 0 # 소수점 아래 자릿수
            while len(strs) > j:
                if strs[j] == '.':
                    if places_cnt < len(strs) - j - 1:
                        places_cnt = len(strs) - j - 1
                    break
                
        self.offset = pow(10,-1*places_cnt)
    
    def setXRange(self, _start, _stop): #xticklabels = xranges
        self.xranges = [setnum for setnum in range(_start, _stop, self.offset)]
        print(self.xranges)
    def setYRange(self, _start, _stop): #yticklabels = yranges
        self.yranges = [setnum for setnum in range(_start, _stop, self.offset)]
        print(self.yranges)
    def setZRange(self, _start, _stop): #zticklabels = yranges
        self.zranges = [setnum for setnum in range(_start, _stop, self.offset)]
        print(self.zranges)
    def setTargetLocate(self, _x, _y, _z):
        """Target object locate setting

        Args:
            _x (double): x axis value
            _y (double): y axis value
            _z (double): z axis value
        """
        self.target_loc=[_x,_y,_z]