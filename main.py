import crawler.bilibilicrawler
import detector.facedetector as fd
from tqdm import tqdm
import os

def main():
    url = 'https://space.bilibili.com/4549624/album'
    ChromeDriverPath = '/snap/chromium/1864/usr/lib/chromium-browser/chromedriver'
    pngs = crawler.bilibilicrawler.crawler(url,ChromeDriverPath)
    path = './data/'
    lst=os.listdir(path)
    tq = tqdm(total=len(lst))
    tq.display()
    for val in lst:
        if val[-4:] != '.jpg' and val[-4:] != '.png': continue
        if fd.detector(path+val):
            os.system('mv '+path+val+' '+path+'pics')
        else:
            os.system('mv '+path+val+' '+path+'useless')
        tq.update()
    

if __name__ == '__main__':
    main()