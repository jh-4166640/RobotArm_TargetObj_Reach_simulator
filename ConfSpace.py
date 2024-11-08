import RobotStatus as Rs
import math

class ConfigurationSpcae(Rs.RobotStatus):
    xranges = []
    yranges = []
    zranges = []
    offset = 0.0
    offset_len = 0
    target_loc = [0,0,0]
    def __init__(self,llen, offset):
        """
        Args:
            llen (list[int]): Length of Links, list size: 5
            offset (float): step for configuration spcace create offset min offset 0.001
        """
        if self.RegisterLink(llen): # RegisterLink error
            return
        strs = str(offset)
        places_cnt = 0
        for i in range(len(strs)):
            if strs[i] == '.':
                places_cnt = len(strs) - i    
                break
        self.offset_len = places_cnt
        self.offset = offset
    def myrange(self, _start,_stop):
        res = _start
        while res<=_stop:
            yield round(res,self.offset_len)
            res+=self.offset
        yield _stop

    def setXRange(self, _start, _stop): #xticklabels = xranges
        self.xranges = [setnum for setnum in self.myrange(_start, _stop)]
        print(self.xranges)
    def setYRange(self, _start, _stop): #yticklabels = yranges
        self.yranges = [setnum for setnum in self.myrange(_start, _stop)]
        print(self.yranges)
    def setZRange(self, _start, _stop): #zticklabels = yranges
        self.zranges = [setnum for setnum in self.myrange(_start, _stop)]
        print(self.zranges)
    def setTargetLocate(self, _x, _y, _z):
        """Target object locate setting

        Args:
            _x (double): x axis value
            _y (double): y axis value
            _z (double): z axis value
        """
        self.target_loc=[_x,_y,_z]

#temp = [10,20,30,40,50.313213]        
#tests = ConfigurationSpcae(temp,0.001)
#tests.setXRange(0,30)
