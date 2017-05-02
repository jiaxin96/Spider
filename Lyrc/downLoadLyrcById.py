#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import  json
import  re
import os
import urllib.response


from  bs4 import BeautifulSoup

def download_start(musicId,name):
    lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(musicId) + '&lv=1&kv=1&tv=-1'
    r = requests.get(lrc_url)
    json_obj = r.text
    j = json.loads(json_obj)

    if ('nolyric' not in j.keys() and 'lrc' in j.keys()):
        if ('lyric' in j['lrc'].keys()):
            lrc=j['lrc']['lyric']
            pat=re.compile(r'\[.*\]')
            lrc = re.sub(pat,"",lrc)
            lrc = lrc.strip()
            writeToTxt(lrc,name,getAuthor(musicId))


def writeToTxt(lrc,name, author):
    if (re.match(r'^[\u4e00-\u9fa5]+', name) == None):
        return

    try:
        if (os.path.exists("ans/author/" + str(author))):
            pass
        else:
            os.mkdir("ans/author/"+ str(author))

        if (os.path.exists("ans/songs/" + str(name) + ".txt")):
            return
        name = re.sub(r'\s$', "", name)
        print(name)
        fo = open("ans/songs/" + str(name) + ".txt", "w+")
        fo.write(str(lrc));
        fo.close()

        fo1 = open("ans/author/"+str(author)+'/'+ str(name) + ".txt", "w+")
        fo1.write(str(lrc));
        fo1.close()
    except:
        return


def getAllListSongId(listId):
    minimumsize = 1
    url = "http://music.163.com/playlist?id=" +str(listId)
    r = requests.get(url)
    contents = r.text
    bsObj = BeautifulSoup(contents,"html.parser")

    songs = bsObj.findAll("a", {"href":re.compile("\/song\?id=[0-9].*")})
    for song in songs:
        download_start(re.sub(r'\/song\?id=', "", song["href"]), song.get_text())


def getAllListId():
    page = 35
    for i in range(50):
        url = "http://music.163.com/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=" + str(page*i)
        r = requests.get(url)
        contents = r.text
        bsObj = BeautifulSoup(contents, "html.parser")
        lists = bsObj.findAll("a", {"href": re.compile("\/playlist\?id=[0-9].*")})
        for list in lists:
            getAllListSongId(re.sub(r'\/playlist\?id=', "", list["href"]))


def getCatlogMusicId():

    return

def search(s, stype=1, offset=0, total='true', limit=60):
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    # NOQA
    }
    action = 'http://music.163.com/api/search/get'
    datas = {
        's': s,
        'type': stype,
        'offset': offset,
        'total': total,
        'limit': limit
    }
    session = requests.Session()
    connection = session.post(action, data=datas, headers=header,timeout=15)
    # of = open("id.cc",'w+')
    # of.write(connection.text)
    # of.close()
    json_obj = connection.text
    j = json.loads(json_obj)
    try:
        lrc = j['result']['songs']
        for l in lrc:
            download_start(l['id'], l['name'])
    except :
        return

def getAuthor(id):
    url = 'http://music.163.com/song?id=' + str(id)
    r = requests.get(url)
    bsObj = BeautifulSoup(r.text, "html.parser")
    name = bsObj.find("a", {"data-res-author": re.compile("^[\u4e00-\u9fa5]+")})
    if (name != None):
        return name['data-res-author']
    return "common"

for i in range(0,1000):
    print(i)
    search(s="民谣", offset=i)