import requests
from  bs4 import BeautifulSoup
import re
def getAuthor(id):
    url = 'http://music.163.com/song?id='+str(id)
    r = requests.get(url)
    bsObj = BeautifulSoup(r.text, "html.parser")
    name = bsObj.find("a", {"data-res-author":re.compile("^[\u4e00-\u9fa5]+")})
    if (name != None):
        return name['data-res-author']
    return "common"