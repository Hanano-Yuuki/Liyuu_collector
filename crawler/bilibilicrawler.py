from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from tqdm import tqdm
import time
import os


def GetAlbums(driver)->list:
    source = driver.page_source
    urls=[]
    while(True):
        pos=source.find('album-card')
        if pos==-1: break
        source=source[pos:]
        beg=source.find('a href=\"')+len('a href=\"')
        source=source[beg:]
        beg=source.find('a href=\"')+len('a href=\"')
        source=source[beg:]
        end=source.find('\" target')
        if source[:2]=='//': urls.append(source[:end])
        source=source[end:]

    target=[]
    path = '/snap/chromium/1864/usr/lib/chromium-browser/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    pngbed = webdriver.Chrome(chrome_options=chrome_options,executable_path=path)
    tq=tqdm(total=len(urls))
    tq.display()
    for items in urls:
        # print(items)
        pngbed.get('https:'+items)
        time.sleep(1)
        src=pngbed.page_source
        while True:
            beg=src.find('background-image: url(&')
            if beg==-1: break
            src=src[beg:]
            beg=src.find('url(&quot;')+len('url(&quot;')
            end=src.find('@')
            target.append(src[beg:end])
            src=src[end:]
        tq.update()
    return target


def GetTotualPages(driver)->int:
    pages = driver.find_element_by_class_name('album-list__pagination')
    idx = str(pages.text)
    beg=idx.find('共 ')+len('共 ')
    end=idx.find(' 页')
    tot=int(idx[beg:end])
    return tot

def GetScreenShot(driver,filename):
    png = driver.get_screenshot_as_png()
    pngfile = open(filename,'wb+')
    pngfile.write(png)
    pngfile.close()


def crawler(url)->list:
    url = 'https://space.bilibili.com/4549624/album'

    path = '/snap/chromium/1864/usr/lib/chromium-browser/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=path)

    driver.get(url)
    time.sleep(1)

    # GetScreenShot(driver,'page-1.png')

    tot=GetTotualPages(driver)

    pngs=[]
    for i in range(tot-1):
        pngs.append(GetAlbums(driver))
        page = driver.find_element_by_class_name('be-pager-next')
        page.click()
        time.sleep(3)
        # GetScreenShot(driver,'page-'+str(i+2)+'.png')
    pngs = [item for sub in pngs for item in sub]
    pngs = list(set(pngs))
    # for png in pngs:
    #     os.system('wget '+png[2:])
    return pngs