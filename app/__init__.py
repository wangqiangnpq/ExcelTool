import xlrd
import os
import math
from config import *
from app.export_tools import Export

def Check_Write_List(filename):
    if not Start_Write_List:
        return True
    for name in Excel_Write_List:
        if filename == name:
            return True
    return False

def Get_Excel_List():
    excel_list = []
    path = Excel_path
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        print("系统找不到指定的路径。  " + path)
        return []
    list = os.listdir(Excel_path)  # 列出文件夹下所有的目录与文件
    for filename in list:
        name =os.path.splitext(filename)
        if name[1] == ".xlsx":
                excel_list.append(name[0])
    return excel_list

def Export_Excel(filename):
    filepath = Excel_path+"\\"+filename+".xlsx"
    if not os.access(filepath, os.F_OK):
        print(filepath + "  文件不存在...")
        return
    elif not os.access(filepath, os.R_OK):
        print(filepath + "  文件不能被读...")
        return
    try:
        book = xlrd.open_workbook(filepath,'utf-8')
    except Exception as e:
        print(filepath + str(e))
        return
    for sheet in book.sheets():
        row_len = len(list(sheet.get_rows()))
        if row_len <= value_row:
            print(filename + "中 " + sheet.name + " 文件行数为[" + str(row_len) + "]不进行操作....")
            return
        if sheet.cell(0, 0).value != Export_Flag:
            print(filename + "中 " + sheet.name + "不进行操作....")
            return
        print(filename + " 开始导出....")
        if Parse_Sheet(filename,sheet):
            print(filename + " 导出成功....")
        else:
            print(filename + " 导出失败....")



def Check_Type_Compair(type, export_type):
    type_dict = type_compair.get(export_type)
    if not type_dict:
        return False
    if not type_dict.get(type):
        return False
    return True

#检查哪些列是可用的
def Get_Use_List(keylist,typelist):
    for i in range(len(keylist)):
        if keylist[i] == "":
            print("     字段名 index =" + str(i+1) + " 不能为空")
            return False
        for l_type in range(0, len(Current_Export_list)):
            check_data = Current_Export_list[l_type]
            if not check_data["checked"]:
                continue
            if not Check_Type_Compair(typelist[i], check_data["type"]):
                print("     字段类型 index =" + str(i+1) + " 没有这个类型")
                return False
    return True


def Check_Data_Type(value, data_type):
    if data_type == Excel_Type.int.value:
        return isinstance(value,int)
    elif data_type == Excel_Type.float.value:
        return isinstance(value,float) or isinstance(value,int)
    elif data_type == Excel_Type.string.value:
        return isinstance(value,str)
    elif data_type == Excel_Type.bool.value:
        return isinstance(value,bool) or value == 1 or value == 0

def Parse_Sheet(filename,sheet):
    key_list = sheet.row_values(key_row)
    data_type_list = sheet.row_values(type_row)
    if not Get_Use_List(key_list,data_type_list):
        return False
    final_value_list = []
    repeat_list = []
    #读取Excel的数据结构
    row_len = len(list(sheet.get_rows()))
    for row in range(value_row,row_len):
        row_list = []
        final_value_list.append(row_list)
        UID = sheet.cell(row, UID_col).value
        if UID in repeat_list:
            print("     重复的唯一标识 "+str(UID))
            return False
        else:
            repeat_list.append(UID)
        for col in range(0,len(key_list)):
            tmp_cell = sheet.cell(row,col)
            tmp_value = tmp_cell.value
            if tmp_cell.ctype == xlrd.book.XL_CELL_NUMBER:
                a,b = math.modf(tmp_value)
                if a == 0.0:
                    tmp_value = int(b)
            elif tmp_cell.ctype == xlrd.book.XL_CELL_TEXT:
                tmp_value = tmp_value
            elif tmp_cell.ctype == xlrd.book.XL_CELL_EMPTY:
                tmp_value = ""
            elif tmp_cell.ctype == xlrd.book.XL_CELL_BOOLEAN:
                tmp_value = tmp_value
            elif tmp_cell.ctype == xlrd.book.XL_CELL_DATE:
                time = xlrd.xldate_as_datetime(tmp_value,0)
                tmp_value = str(time)
            if not Check_Data_Type(tmp_value, data_type_list[col]):
                print("     row =" + str(row+1) + ", col="+str(col+1)+" 的数据类型不正确!")
                return False
            row_list.append(tmp_value)
    #导出文件
    for i in range(0, len(Current_Export_list)):
        export_type_list = Current_Export_list[i]
        try:
            Export(filename, key_list, data_type_list, final_value_list, export_type_list)
            print("     " + filename + " 导出[" + Current_Export_list[i]["type"] + " ]成功")
        except Exception as e:
            print("     " + filename + " 导出[" + Current_Export_list[i]["type"] + " ]失败 " + str(e))
    return True


def Export_All_Excel(excel_list):
    list = []
    for name in excel_list:
        if Check_Write_List(name+".xlsx"):
            list.append(name)
            Export_Excel(name)
    if len(list) == 0:
        print("没有找到要导出的表,请重新选择")
        print("")
        Get_User_Scan()
        return
    print("*******************导出结束**********************")


def Get_User_Scan():
    print("选择要导出的表:")
    print("1 = 全部导出")
    print("2 = 输入你想要导出的表【xxx1,xxx2】")
    itype = input('请输入导出类型:')
    if itype == "1":
        print("全部Excel导出中....")
        excel_list = Get_Excel_List()
        Export_All_Excel(excel_list)
    elif itype == "2":
        excel = input('请输入Excel名:')
        excel_list = excel.split(',')
        Export_All_Excel(excel_list)
    else:
        print("")
        print("类型输入错误,请重新选择")
        Get_User_Scan()





