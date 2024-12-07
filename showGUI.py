import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import ErrorDoc as erd
import ConfSpace as conf
import RobotPose as rp
import numpy as np
from XslxData import writeEXCELW
def resetEntry():
    global init_entrys
    global target_entrys
    global linkset_entry
    for i in range(len(linkset_entry)):
        linkset_entry[i].delete(0,'end')
    for i in range(len(init_entrys)):
        init_entrys[i].delete(0,'end')
    for i in range(len(target_entrys)):
        target_entrys[i].delete(0,'end')

def simulationFrame(update, tp, run=0):
    plt.cla()
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    canvas = FigureCanvasTkAgg(fig,master=simFrame)
    canvas.get_tk_widget().grid(row=0,column=0)
    if update:
        ax.cla()
        xs = mypos[:, 0]
        ys = mypos[:, 1]
        zs = mypos[:, 2]
        if run == 1:   
            ax.scatter(tp[0],tp[1],tp[2],marker='D',c='red',s=30)
        ax.plot(xs, ys, zs, '-o', markersize=7, markerfacecolor='green', linewidth=2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-myconf.maxval,myconf.maxval)
        ax.set_ylim(-myconf.maxval,myconf.maxval)
        ax.set_zlim(-myconf.maxval,myconf.maxval)
        canvas.draw()
def settingFrame(): # robot setting and create part
    global linkset_entry
    #------------------------------------createRobot---------------------------------------#
    def createRobot():
        global myconf
        global robotpose
        global mypos
        for i in range(0,len(linkset_entry)):
            if erd.input_NOT_NUM_data("link setting",linkset_entry[i].get()):
                return
        for i in range(0,len(svset_entry_min)):
            if erd.input_NOT_NUM_data("servo setting",svset_entry_min[i].get()):
                return
            if erd.input_NOT_NUM_data("servo setting",svset_entry_max[i].get()):
                return
            if int(svset_entry_max[i].get()) < int(svset_entry_min[i].get()):
                erd.Range_ERROR()
                return
        if erd.input_NOT_NUM_data("unit angle",angleunit.get()):
            return
        linklist = []
        for i in range(0,3): #4 3 2 1
            linklist.append(int(linkset_entry[2-i].get()))
        offset = int(angleunit.get())
        myconf = conf.ConfigurationSpcae(linklist, offset)
        myconf.setSpaceRange()
        cur_angle = []  
        for i in range(0, myconf._joint_number):
            min = int(svset_entry_min[myconf._joint_number-1-i].get())
            max = int(svset_entry_max[myconf._joint_number-1-i].get())
            myconf.set_AngleRange(i,min,max)
            cur_angle.append(int(svset_entry_min[myconf._joint_number-1-i].get()))
        robotpose = rp.RobotPose(myconf.link_length,cur_angle)
        mypos = robotpose.Forward_Kinematics()
        simulationFrame(update=True,tp=0)
        print("create robot")
    
    #--------------------------------------------------------------------------------------#
    setFrame = tk.Frame(mainwindows,padx=50, width=200,height=750)
    setFrame.grid(row=0,column=1)
    setlabels = [tk.Label(setFrame, text="Link length setting"), tk.Label(setFrame, text="Servo enable angle setting"),
                 tk.Label(setFrame, text="unit angle")]
    linkset_labels = [tk.Label(setFrame,text="Top to End-effector"),
                      tk.Label(setFrame,text="Mid to Top"),
                      tk.Label(setFrame,text="Bottom to Mid")]
    linkset_entry = [tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10)]
    svset_labels = [tk.Label(setFrame,text="End-Effector Servo angle"), tk.Label(setFrame,text="Wrist Servo angle"),
                    tk.Label(setFrame,text="Top Servo angle"),tk.Label(setFrame,text="Mid Servo angle"),
                    tk.Label(setFrame,text="Bottom Servo angle"),tk.Label(setFrame,text="Base Servo angle")]
    svset_entry_min = [tk.Entry(setFrame,width=10,),tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),
                    tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10)]
    svset_entry_max = [tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),
                    tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10),tk.Entry(setFrame,width=10)]
    svset_entry_min[0].insert(0,"0")
    svset_entry_max[0].insert(0,"90")
    svset_entry_min[1].insert(0,"0")
    svset_entry_max[1].insert(0,"360")
    svset_entry_min[0].config(state=tk.DISABLED)
    svset_entry_max[0].config(state=tk.DISABLED)
    svset_entry_min[1].config(state=tk.DISABLED)
    svset_entry_max[1].config(state=tk.DISABLED)
    for i in range(2,6):
        svset_entry_min[i].insert(0,"-360")
        svset_entry_max[i].insert(0,"360")
        svset_entry_min[i].config(state=tk.DISABLED)
        svset_entry_max[i].config(state=tk.DISABLED)
    setlabels[0].grid(row=0,column=0,columnspan=2)
    for i in range(0,3):
        linkset_labels[i].grid(row=i+1,column=0)
        linkset_entry[i].grid(row=i+1,column=1)
    tk.Label(setFrame, text="", borderwidth=1, padx=10, pady=10).grid(row=6,column=0,rowspan=2)    
    setlabels[1].grid(row=8,column=0,columnspan=3)
    angleunit_item = [1, 2, 3, 4, 5, 6, 7, 8, 9 ,10]
    angleunit = ttk.Combobox(setFrame,width=10, height=10,values=angleunit_item)
    angleunit.set("5")
    setlabels[2].grid(row=9,column=0)
    angleunit.grid(row=9,column=1)
    tk.Label(setFrame, text="", borderwidth=1, padx=10, pady=3).grid(row=10,column=0)    
    tk.Label(setFrame,text="min angle").grid(row=11,column=1)
    tk.Label(setFrame,text="max angle").grid(row=11,column=2)
    for i in range(0,6):
        svset_labels[i].grid(row=i+13,column=0)
        svset_entry_min[i].grid(row=i+13,column=1)
        svset_entry_max[i].grid(row=i+13,column=2)
    tk.Label(setFrame, text="", borderwidth=1, padx=10, pady=10).grid(row=23,column=0,rowspan=2)    
    set_btns = tk.Button(setFrame,text="create",width=10,height=3,font= '13', foreground='yellow', bg="blue", command=createRobot)
    set_btns.grid(row=25,column=0, columnspan=2)
    reset_btns = tk.Button(setFrame,text="reset",width=10,height=3,font= '13', foreground='white', bg="red", command=resetEntry)
    reset_btns.grid(row=25,column=2, columnspan=2)

def runningFrame(): # program run part
    global init_entrys
    global target_entrys
    def pre_step():
        global myconf
        global robotpose
        global mypos
        global step_index
        global angle_list
        if step_index-1 < 0:
            step_index=0
            return
        step_index -= 1
        robotpose.setParam(myconf.link_length,angle_list[step_index])
        mypos = robotpose.Forward_Kinematics()
        simulationFrame(update=True,tp=myconf.getTargetLocate(),run=1)
    def next_step():
        global myconf
        global robotpose
        global mypos
        global step_index
        global angle_list
        if step_index+1 >= len(angle_list):
            step_index=len(angle_list)-1
            return
        step_index += 1
        robotpose.setParam(myconf.link_length,angle_list[step_index])
        mypos = robotpose.Forward_Kinematics()
        simulationFrame(update=True,tp=myconf.getTargetLocate(),run=1)
    def runFindTarget():
        global myconf
        global robotpose
        global mypos
        global step_index
        global angle_list
        for i in range(0,len(init_entrys)):
            if erd.input_NOT_NUM_data("initialize angle",init_entrys[i].get()):
                return
        for i in range(0, len(target_entrys)):
            if erd.input_NOT_NUM_data("Target Positon", target_entrys[i].get()):
                return
        if np.sqrt((int(target_entrys[0].get()))**2 + (int(target_entrys[1].get()))**2 + (int(target_entrys[2].get()))**2) > myconf.maxval:
            diff = np.sqrt((int(target_entrys[0].get()))**2 + (int(target_entrys[1].get()))**2 + (int(target_entrys[2].get()))**2) - myconf.maxval
            erd.Target_OVER_location_error(diff)
            return 
        try:    
            myconf.setTargetLocate(int(target_entrys[0].get()),int(target_entrys[1].get()),int(target_entrys[2].get()))
            cur_angle = []
            for i in range(0, len(init_entrys)):
                cur_angle.append(int(init_entrys[myconf._joint_number-1-i].get()))           
            robotpose.setParam(myconf.link_length,cur_angle)
            find_angle=robotpose.Inverse_Kinematics(myconf.getTargetLocate(),myconf.link_length,myconf.motor_angle_range)
            print("find_angle ", find_angle)
            if find_angle == False:
                erd.Target_OVER_ANGLE_error()
            #robotpose.setParam(myconf.link_length,myangle)
            #mypos = robotpose.Forward_Kinematics()
            simulationFrame(update=True,tp=myconf.getTargetLocate(),run=1)
            angle_list=robotpose.show_ROBOT_MOVEMENT(cur_angle, find_angle, myconf.getUnitOffset())
            if angle_list != False:
                step_index=0
                sim_btns = [tk.Button(runFrame,text="<",width=5,height=3,font= '13', foreground='black',command=pre_step),
                            tk.Button(runFrame,text=">",width=5,height=3,font= '13', foreground='black',command=next_step)]
                sim_btns[0].grid(row=17,column=0)
                sim_btns[1].grid(row=17,column=1)
                print("Run")
        except:
            erd.NOT_CREATE_ROBOT()
    
        
    runFrame = tk.Frame(mainwindows,padx=50, width = 200, height=750)
    runFrame.grid(row=0,column=2)
    labels = [tk.Label(runFrame, text="Position Initialize"), tk.Label(runFrame, text="Target Coordinate")]
    init_labels = [tk.Label(runFrame,text="End-Effector Servo angle"), tk.Label(runFrame,text="Wrist Servo angle"),
                tk.Label(runFrame,text="Top Servo angle"),tk.Label(runFrame,text="Mid Servo angle"),
                tk.Label(runFrame,text="Bottom Servo angle"),tk.Label(runFrame,text="Base Servo angle")]
    init_entrys = [tk.Entry(runFrame,width=10), tk.Entry(runFrame,width=10), tk.Entry(runFrame,width=10),
                tk.Entry(runFrame,width=10),tk.Entry(runFrame,width=10),tk.Entry(runFrame,width=10)]
    target_labels=[tk.Label(runFrame,text="target x"), tk.Label(runFrame,text="target y"),
                tk.Label(runFrame,text="target z")] 
    target_entrys = [tk.Entry(runFrame,width=10), tk.Entry(runFrame,width=10), tk.Entry(runFrame,width=10)]
    tk.Label(runFrame, text="", borderwidth=1, padx=10, pady=10).grid(row=1,column=0,columnspan=2)
    labels[0].grid(row=2,column=0,columnspan=2)
    for i in range(0, 6):
        init_labels[i].grid(row=i+3,column=0,padx=10)
        init_entrys[i].grid(row=i+3,column=1,padx=10)
    init_entrys[0].insert(0,"0")
    init_entrys[1].insert(0,"0")
    init_entrys[0].config(state=tk.DISABLED)
    init_entrys[1].config(state=tk.DISABLED)
    tk.Label(runFrame, text="", borderwidth=1, padx=10, pady=10).grid(row=9,column=0,columnspan=2)
    labels[1].grid(row=10,column=0,columnspan=2)
    for i in range(0,3):
        target_labels[i].grid(row=i+11,column=0,padx=10)
        target_entrys[i].grid(row=i+11,column=1,padx=10)
    tk.Label(runFrame, text="", borderwidth=1, padx=10, pady=10).grid(row=14,column=0,rowspan=2,columnspan=2)
    run_btn = tk.Button(runFrame,text="Run",width=10,height=3,font= '13', foreground='white', bg="green", command=runFindTarget)
    run_btn.grid(row=16,column=0)
    
    

mainwindows = tk.Tk()
mainwindows.title("6-dof Robot-Arm 4-dof movement simulator")
mainwindows.geometry("1700x900")
mainmenu = tk.Menu(mainwindows)
filemenu = tk.Menu(mainmenu)
try:
    filemenu.add_command(label='save', command=lambda: writeEXCEL(angle_list))
except:
    print("undefined angle_list")
mainmenu.add_cascade(label="File",menu=filemenu)
mainwindows.config(menu=mainmenu)
simFrame = tk.Frame(mainwindows,width=100,height=1000,bg="white")
simFrame.grid()
simulationFrame(update=False, tp=0)
settingFrame()
runningFrame()


mainwindows.mainloop()
