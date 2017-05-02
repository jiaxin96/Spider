import urllib.request
html = urllib.request.urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())