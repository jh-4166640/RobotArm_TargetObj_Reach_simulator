import tkinter.messagebox as msg

def input_NOT_NUM_data(ent,_data):
    try:
        int(_data)
    except:
        msg.showerror('Type Error', ent + " data is not Numerical!")
        return 1
def input_NULL_data(ent,_data):
    if _data == "":
        msg.showerror('Type Error', ent + " data is NULL!")
        return 1
def Range_ERROR():
    msg.showerror('Range Error',"min > max Error!")
def index_OutofRange():
    msg.showerror('Index Error',"OutofRange!")
def LinkList_size_error():
    msg.showerror('Link Error',"Link list size error")
def Target_OVER_location_error():
    msg.showerror('Target Error',"can't reach point")
def Target_OVER_ANGLE_error():
    msg.showerror('Angle Error',"can't angle range of operation!")
def NOT_CREATE_ROBOT():
    msg.showerror('Create Error',"must create robot!")