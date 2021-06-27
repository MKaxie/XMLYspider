import os
import requests
import threading
import json

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

# url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=45242408&pageNum=1'# 少年白马醉春风

def getaudio(title,id,savedir): # 获取音频数据

    title = title.replace('/',' ') # 防止保存失败
    url = f'https://www.ximalaya.com/tracks/{id}.json' # 音频信息json接口

    rps = requests.get(url=url,headers=headers)
    content = rps.content.decode('utf-8')
    data = json.loads(content)
    audiopath = data["play_path_64"] # 音频地址

    audiodata = requests.get(audiopath)

    with open(f'{savedir}/{title}.m4a','wb+') as fp:
        fp.write(audiodata.content)

    print(title,'is ok!')


def getPage(albumid,pageid): # 获取单页专辑列表
    # 专辑音频列表json接口
    url = f'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={albumid}&pageNum={pageid}'
    rps = requests.get(url=url,headers=headers)
    content = rps.content.decode('utf-8')
    data = json.loads(content)

    info_list = data["data"]["tracks"]
    albumTitle = data["data"]["tracks"][0]["albumTitle"]

    savedir = f'./{albumTitle}' # 获取专辑名称
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    for item in info_list:
        trackid = item["trackId"]
        title = item["title"]

        getaudio(title,trackid,savedir)

def spiderXM(albumid,pagenums):

    # albumid: 专辑id
    # pagenums: 音频页数

    threads = []

    for i in range(pagenums):
        # 创建线程
        t = threading.Thread(target=getPage, args=(albumid, i + 1,))
        t.start()
        threads.append(t)
    # 等待所有线程执行完毕
    for t in threads:
        t.join()


if __name__ == '__main__':

    spiderXM(22088302,4) # 西游记

    print('抓取完毕！')
