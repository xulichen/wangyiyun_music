# wangyiyun_music
网易云音乐 歌手top50

# 利用selenium抓取网易云音乐内热门歌手的前50首歌曲
并储存至mongoDB

# 所需python库

1. selenium
2. pymongo

由于网易云音乐网页的内部构造，需要抓取的内容是在iframe内部。
简单的静态网页抓取已经不能够完成基本信息的提取，因此需要利用
selenium内switch_to.frame()来切换至iframe内部提取内容。
