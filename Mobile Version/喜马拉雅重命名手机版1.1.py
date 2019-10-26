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

print("喜马拉雅重命名手机版1.1")
print("注意事项:")
print("目录选择存放音频文件的那个目录")
print("必须输入ximalaya.db的绝对路径，也就是全路径")
print("文件后如果没有后缀名可以直接回车，如果已经解密或转换为其他格式文件，则输入转换后的文件类型")
print("此程序在2019年10月12日时仍然有效，若失效请联系xyz.hack666@gmail.com")
print()
#safe file name
illegal_Char = re.compile(r"[/\\:*?\"<>|]") 
#fetch encryption name from savepath
file_name_flag = re.compile("/([^/]+)")

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
            sql = """select downloadedsavefilepath,tracktitle from track"""
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
                    
                    
print("2019.10.12")
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


    
    
    
    
    
