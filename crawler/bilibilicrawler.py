from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import wget
import os


def GetAlbums(driver,datatable=[]):
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
    for i,items in enumerate(urls):
        # print(items)
        pngbed.get('https:'+items)
        # time.sleep(1)
        WebDriverWait(pngbed,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'main-content')))
        src=pngbed.page_source
        while True:
            beg=src.find('background-image: url(&')
            if beg==-1: break
            src=src[beg:]
            beg=src.find('url(&quot;')+len('url(&quot;')
            end=src.find('@')
            target_check = src[beg:end]
            if target_check[2:] in datatable:
                print('\nHit Database Record!')
                return (True,target)
            target.append(src[beg:end])
            src=src[end:]
        print('\t%d/%d' % (i+1,len(urls)),end='\r')
    return (False,target)


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


def crawler(url,driverpath,datatable)->list:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=driverpath)

    driver.get(url)
    # time.sleep(1)
    WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'album-card__picture')))

    # GetScreenShot(driver,'page-1.png')

    tot=GetTotualPages(driver)

    pngs=[]
    for i in range(tot):
        print('page %d/%d      ' % (i+1,tot),end='\n')
        flag,ans = GetAlbums(driver,datatable)
        pngs.append(ans)
        if flag: break
        if i==tot-1: break
        page = driver.find_element_by_class_name('be-pager-next')
        page.click()
        # time.sleep(3)
        WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'album-card__picture')))
        # GetScreenShot(driver,'page-'+str(i+2)+'.png')
    pngs = [item[2:] for sub in pngs for item in sub]
    pngs = list(set(pngs))
    # for png in pngs:
        # os.system('wget '+png[2:])
        # wget.download(png[2:],out='./data/')
    return pngs