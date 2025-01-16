from openpyxl import Workbook

def writeEXCEL(angle_list):
    write_wb = Workbook()
    write_ws = write_wb.create_sheet('angle_data set')
    write_ws = write_wb.active
    for myangle in angle_list:
        write_ws.append(myangle)
    write_wb.save(filename='RobotArmAngleData.xlsx')
    