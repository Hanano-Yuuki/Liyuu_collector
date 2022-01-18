import crawler.bilibilicrawler
import detector.facedetector as fd
import os
import wget

def saveDB(path,datas,mode='w+'):
    with open(path,mode) as f:
        for line in datas:
            print(line,sep='\n',file=f)


def loadDB(path)->list:
    if not os.path.exists(path):
        print('Initialize Database: %s' % path)
        os.mknod(path)
    ret=[]
    with open(path,'r') as f:
        while True:
            line = f.readline()
            if not line: break
            ret.append(line[:-1])
    return ret


def main():
    url = 'https://space.bilibili.com/4549624/album'
    ChromeDriverPath = '/snap/chromium/1864/usr/lib/chromium-browser/chromedriver'
    InternalDBPath = './DataBases/Liyuu_Internal.DB'
    DBPath = './DataBases/Liyuu.DB'
    dt = loadDB(InternalDBPath)
    # print(dt)
    pngs = crawler.bilibilicrawler.crawler(url,ChromeDriverPath,dt)
    que = []
    for p in pngs:
        dt.append(p)
        pic_url = wget.download('https://'+p,out='./tmp')
        if fd.detector(pic_url):
            print('...accept')
            que.append(p)
        else:
            print('...reject')
        os.remove(pic_url)
    saveDB(InternalDBPath,dt)
    saveDB(DBPath,que,'a+')
    print('program exit.')
    

if __name__ == '__main__':
    main()