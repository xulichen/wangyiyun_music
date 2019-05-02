from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import re
from config import *

t3 = 't3'
cilent = pymongo.MongoClient(t3)
db = cilent[MONGO_DB]

# 切换为phantomJS无界面阅览器
# driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# driver.set_window_size(2880, 1800)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

# 切换到iframe框架下
def get_frame(url):
    driver.get(url)
    driver.switch_to.frame('g_iframe')
    return driver


# 索引页检索热门歌手及其主页
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


# 歌手名字
def get_url(name):
    # name = input('歌手名字：')
    url = dic[name]
    return url


# 歌手主页提取歌曲名，歌曲时间及url
def get_music(name, urls):
    try:
        driver = get_frame(urls)
        music_name = driver.find_elements_by_xpath('//tbody/tr/td[2]/div/div/div/span/a/b')
        music_url = driver.find_elements_by_xpath('//tbody/tr/td[2]/div/div/div/span/a')
        music_time = driver.find_elements_by_xpath('//tbody/tr/td[3]/span')
        info_list = []
        for i in range(len(music_name)):
            info = {
                'music_name': music_name[i].text,
                'music_time': music_time[i].text,
                'music_url': music_url[i].get_attribute('href')
            }
            info_list.append(info)
        return info_list

    except TimeoutException:
        get_music(name, urls)


# 进入歌曲主页提取评论
def get_comment(name, info_list):
    for info in info_list:
        comment_url = info.get('music_url')
        driver = get_frame(comment_url)
        comment_html = driver.page_source
        comments = re.findall('<div class="cnt f-brk".*?<a href.*?class.*?>(.*?)</a>(.*?)</div>', comment_html)
        join_cmt = []

        for i in comments:
            i[1].replace('<br>', '')
            join_cmt.append(i[0] + i[1].replace('<br />', ''))

        info['comment'] = join_cmt[0:5]
        save_to_mongo(name, info)


# 存进mongodb
def save_to_mongo(name, result):
    try:
        if db[name].insert(result):
            print('储存成功', result)
    except Exception:
        print('储存失败')


def main():
    dic = get_index()
    for i in dic:
        url = get_url(i)
        info_list = get_music(i, url)
        get_comment(i, info_list)


if __name__ == '__main__':
    main()

