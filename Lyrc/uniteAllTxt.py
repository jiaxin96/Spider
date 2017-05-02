#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import os.path

rootdir = "ans/songs"                             # 指明被遍历的文件夹

for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    ofD = open("AllInOne/ans.txt", 'a+')
    for filename in filenames:
        print(filename)
        ofS = open(rootdir + "/" + filename, 'r')
        ofD.write(ofS.read())
        ofS.close()
    ofD.close()
