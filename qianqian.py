import requests
from urllib.parse import urlencode
import re
import os
from lxml import etree
import json


#'http://music.taihe.com/artist/1097'
#http://music.taihe.com/song/931434
#http://music.taihe.com/mv/931434
#http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17205094400219614135_1565323062145&songid=931434
#http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17208087768768543488_1565332983989&songid=299800



def downmusic(url):
    mp3 = {}
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    respond=requests.get(url,headers=header)
    html =respond.content.decode('utf-8')
    js=json.loads(html)
    doc =js['data']["html"]
    hm=etree.HTML(doc)
    name=hm.xpath('//span[@class="songname"]/a[1]/text()')
    href = hm.xpath('//span[@class="songname"]/a[1]/@href')



    for h,n in zip(href,name):
    #     #http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17205094400219614135_1565323062145&songid=490260&from=web
        j=h.strip('/song/ ')

        h='http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17205094400219614135_1565323062145&songid=' + j+"&from=web"

        n=n.replace(':','').replace('?','').replace('*','').replace('|','').replace('/','').replace('\\','').replace(' ','')
        json1=requests.get(h,headers=header)
        js=json1.content.decode('utf-8')
        try:
            ha=re.findall('file_link":"(.*?)"',js)[0].replace('\\','')
        except:
            print("版权原因无法下载！")
        if n in mp3:
            n=n+"(1)"
            mp3[n] = ha
        else:
            mp3[n]=ha

    return mp3
if __name__ == '__main__':
    for i in [0,15,30,45]:
        url="http://music.taihe.com/data/user/getsongs?start="+"600"+"&size=15&ting_uid=1097"
        mp3=downmusic(url)
        t=1
        for key in mp3:
            num=600+t
            os.system(r'you-get -o D:\ee\mp3 -O {} {}'.format(str(num)+'、'+key, mp3[key]))
            i+=1