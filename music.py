from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pymongo
from config import *

cilent = pymongo.MongoClient(MONGO_URL)
db = cilent[MONGO_DB]
driver = webdriver.Chrome()


def get_frame(url):
    driver.get(url)
    driver.switch_to.frame('g_iframe')
    return driver


def get_index():
    try:
        driver = get_frame('http://music.163.com/discover/artist')
        artist_name = driver.find_elements_by_xpath('//li[@class="sml"]/a[1]')
        dicts = {}
        for i in artist_name:
            dicts[i.text] = i.get_attribute('href')
        print(dicts)
        return dicts
    except TimeoutException:
        get_index()



def get_url(name):
    # name = input('歌手名字：')
    url = dic[name]
    return url


def get_music(name, urls):
    try:
        driver = get_frame(urls)
        music_name = driver.find_elements_by_xpath('//tbody/tr/td[2]/div/div/div/span/a/b')
        music_url = driver.find_elements_by_xpath('//tbody/tr/td[2]/div/div/div/span/a')
        music_time = driver.find_elements_by_xpath('//tbody/tr/td[3]/span')
        for i in range(len(music_name)):
            info = {
                'music_name': music_name[i].text,
                'music_time': music_time[i].text,
                'music_url': music_url[i].get_attribute('href')
            }
            print(info)
            save_to_mongo(name, info)
    except TimeoutException:
        get_music(name, urls)


def save_to_mongo(name, result):
    try:
        if db[name].insert(result):
            print('储存成功', result)
    except Exception:
        print('储存失败')


if __name__ == '__main__':
    dic = get_index()
    for i in dic:
        url = get_url(i)
        get_music(i, url)