# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:46:25 2019

@author: xyz
"""

#table track downloadedsavefilepath   tracktitle 
# coding:utf-8
import re
import os
import sqlite3

#Description

print("喜马拉雅重命名手机版1.1.2")
print("注意事项:")
print("选择喜马拉雅app的版本，因为我也不清楚到底哪个版本开始有更改，所以只能做一个大概的描述")
print("目录选择存放音频文件的那个目录")
print("必须输入ximalaya.db的绝对路径，也就是全路径")
print("文件后如果没有后缀名可以直接回车，如果已经解密或转换为其他格式文件，则输入转换后的文件类型")
print("此程序在2019年11月3日时仍然有效，若失效请联系xyz.hack666@gmail.com")
print()

#safe file name
illegal_Char = re.compile(r"[/\\:*?\"<>|]") 
#fetch encryption name from savepath
file_name_flag = re.compile("/([^/]+)")

version = 0;
while(version != 1 or version != 2):
    print("1.版本 5.4.27.3 左右")
    print("2.版本 6.6.21.3 左右")
    try:
        version = int(input("请输入选择（1或2）:"))
    except Exception as e:
        print("请重新输入选择!")
    print("")
    
#get operational dir
dirname = input("请输入音频所在的目录名：")
print("")
dirname = dirname.replace("/","\\")
dirname = dirname.replace("\"","")
dirname = dirname.replace("'","")

try:
    os.chdir(dirname)
except OSError as err:
    print("系统错误: {0}".format(err))
    print("")
else:    

    #get ximalaya.db path
    ximalayadb = input("输入ximalaya.db含路径全名：")
    print("")
    ximalayadb = ximalayadb.replace("/","\\")
    ximalayadb = ximalayadb.replace("\"","")
    ximalayadb = ximalayadb.replace("'","")
    
    #connect to db
    try:
        conn = sqlite3.connect(ximalayadb)
        cursor = conn.cursor()
    except Exception as err:
        print(err)
    else:
        
        #select original encryption name and original name
        try:
            if(version == 1):
                sql = """select downloadedsavefilepath,tracktitle from track"""
            elif(version == 2):
                sql = """select downloadedsavefilepath,tracktitle from newtrack"""
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as err:
            print(err)
            
        #process(fetch name and rename file)
        else:
            
            file_extension = input("输入文件后缀名（无后缀名直接回车）：")
            print("")
            file_extension = file_extension.replace("/","\\")
            file_extension = file_extension.replace("\"","")
            file_extension = file_extension.replace("'","")
            file_extension = file_extension.replace(".","")
                   
            for element in result:
                download_name = re.findall(file_name_flag,element[0])[-1]
                title = re.sub(illegal_Char,"",element[1])
                newname = title + "." + file_extension
                if(os.path.isfile(newname)):
                    newname = title + element[0] + "." + file_extension
                
                try:
                    os.rename(download_name, newname)
                except Exception as err:
                    print("无法重命名文件: ",download_name, " 到: ",newname, " 原因: ",err)
                    print("")
                    
                    
print("2019.11.3")
print("------xyz")    
os.system("pause")
'''
sql = """select name from sqlite_master where type='table' order by name"""
cursor.execute(sql)
result = cursor.fetchall()
print(result)
print(type(result))
'''

'''
sql = """pragma table_info(track)"""
cursor.execute(sql)
result = cursor.fetchall()
print(result)
print(type(result))
'''
'''
sql = """select * from track"""
cursor.execute(sql)
result = cursor.fetchall()
print(result)
print(type(result))
'''


    
    
    
    
    
