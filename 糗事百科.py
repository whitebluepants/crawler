import re
import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('HTML Exception')
        return ''
    
def getArtList(lst,imglst,url,page):
    count = 0
    for i in range(page):
        try:
            html = getHTMLText(url + str(i + 1))
            soup = BeautifulSoup(html,'html.parser')
            d = soup.find('div',id = 'content-left').children
            for art in d:
                if art.name == 'div':
                    try:
                        t = art.find('div',{'class':'content'})
                        count += 1
                        text = str(count) + " " + t.span.text.strip()
                        if art.find('div',{'class':'thumb'}):
                            img = art.find('img',{'class':'illustration'}).attrs['src']
                            text = text +  ' [' + str(count) + img[-4:] + ']'
                            imglst[count] = img
                        lst.append(text)
                    except:
                        print('GET Exception')
                        continue
        except:
            print('EXCEPTION')
            continue

def printList(lst,imglst,path):
    p = r'C:/Users/WhiteBlue Pants/Desktop/qiu/'
    for i in range(len(lst)):
        try:
            with open(path,'a') as file:
                file.write(lst[i] + '\n\n')
                if imglst[i + 1]:
                    img = requests.get('http:' + imglst[i + 1])
                    with open(p + str(i + 1) + imglst[i + 1][-4:],'wb') as file:
                        file.write(img.content)
            print('\r当前进度:{:.2f}%'.format( (i+1)*100 / len(lst) ), end = '')
        except:
            print('\r当前进度:{:.2f}%'.format( (i+1)*100 / len(lst) ), end = '')
            #print('Print Exception')

def main():
    path = r'C:/Users/WhiteBlue Pants/Desktop/qiu/qiu.txt'
    url = 'https://www.qiushibaike.com/8hr/page/'
    spage = 2
    qlist = []
    imglist = {}
    getArtList(qlist,imglist,url,spage)
    printList(qlist,imglist,path)

main() 
