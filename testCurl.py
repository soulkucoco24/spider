import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re

hosturl = "	www.xiguaji.com"
posturl = "http://www.xiguaji.com/Login/Login"

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

headers = {
           'Accept': "application/json, text/javascript, */*; q=0.01",
           'Accept-Encoding': "gzip, deflate",
           'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
           'Host' : 'www.xiguaji.com',
           # 'Cookie' : 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; XIGUA=UserId=103dad732c906557; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225',
           'Cookie' : 'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1470892898,1470972121,1471082145,1471226103; XIGUASTATE=XIGUASTATEID=e2296ebbeaf74e1890ff15c2b981ba20; chl=key=FromBaiDu&word=6KW/55Oc5YWs5LyX5Y+35Yqp5omL; ASP.NET_SessionId=u4vxqxryrcwf4yokqfunswpu; XIGUA=UserId=103dad732c906557; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1471253237',
           'Referer' : 'http://www.xiguaji.com/Login',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
           'X-Requested-With' : 'XMLHttpRequest'
           }

postData = {
    'email' : "18616152909",
    'password' : "norman92",
    'chk' : "6ebbea"
}

postData = urllib.urlencode(postData)

request = urllib2.Request(posturl, postData, headers)
print request
response = urllib2.urlopen(request)
text = response.read()
cookie = cj._cookies
print text
print cookie