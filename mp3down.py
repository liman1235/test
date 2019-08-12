import requests
from urllib.parse import urlencode
import re
import os
from lxml import etree
# url="http://www.htqyy.com/top/musicList/hot?pageIndex=1&pageSize=20"
#mp3="33/mp3/8

def main(offic,i):

    mp3url=[]
    base_url='http://www.htqyy.com/top/musicList/hot?'
    param={
        'pageIndex':offic,
        'pageSize':20
    }
    url=base_url+urlencode(param)

    respond=requests.get(url)
    html=respond.content.decode('utf-8')

    pa=re.compile('sid="(.*?)"')
    sid=re.findall(pa,html)

    def music(sid):
        u="http://www.htqyy.com/play/{}".format(sid)
        rty = requests.get(u)
        hiy = rty.content.decode('utf-8')
        p = re.compile('mp3="(.*?)"')
        new=re.findall(p,hiy)
        return new

    doc=etree.HTML(html)
    name=doc.xpath('//ul[@id="musicList"]//span[@class="title"]/a/text()')
    n=0
    for id in sid:
        neid=music(id)
        mp3="http://f2.htqyy.com/play7/{}".format(neid[0])
        # print(mp3)
        tit=name[n].replace(':','').replace('?','').replace('*','').replace('|','').replace('/','').replace('\\','').replace(' ','')
        n+=1
        os.system(r'you-get -o D:\ee\mp3 -O {} {}'.format(str(i+1)+"、"+tit, mp3))
        i+=1
i=0
for a in range(1,4):
    main(a,i)
    i = i + 20
