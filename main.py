import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import re
import threading
import time
from queue import Queue

import requests
from moviepy.editor import *

import tangdou
from get_vid import get_vid_set
from headers import headers

import signal

downloading = False

def downloader(name, url, path):
    global downloading
    if not os.path.exists(path):
        raise ValueError("'{}' does not exist".format(path))
    start = time.time()  # Download start
    header = headers(url).buildHeader()
    response = requests.get(url, headers=header, stream=True)
    size = 0  # Downloaded file size
    chunk_size = 1024 * 1024  # data size per download
    content_size = int(response.headers["content-length"])  # Total download file size
    if response.status_code == 200:  # Download succesful
        filepath = os.path.join(path, name + ".mp4")
        if os.path.exists(filepath) and os.path.getsize(filepath) == content_size:
            print(f"{name}.mp4 already exists")
            return
        with open(filepath, "wb") as file:  # Show prograss bar
            print(f"{name}.mp4 {content_size / 1024 / 1024:.2f}MB downloading...")
            downloading = True
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)
            downloading = False
        end = time.time()  # Download completed
        if os.path.exists(filepath):
            print(f"{name}.mp4 download completed, time: {end - start:.2f}s")
        else:
            raise OSError("Download error, {} does not exist".format(filepath))
    else:
        raise RuntimeError("request error, error code:", response.status_code)


def time_check(time_str):
    """convert time string to tuple and check its format
    :param str: the time string with ' ', '.', ':', '：', ',' and '，' as delimiter
    :param return: return a tuple that looks like (hour, minute, second) if the
    input format is correct, otherwise return None
    """
    splitted = re.split(" |\.|:|：|,|，", time_str)
    if len(splitted) > 3:
        return None

    time = [0, 0, 0]
    limit = (60, 60, 24)  # Reversed
    splitted.reverse()  # Reverse order traversal
    for i in range(len(splitted)):
        tmp = splitted[i]
        if tmp.isdigit() and int(tmp) < limit[i]:
            time[i] = int(tmp)
        else:
            return None

    time.reverse()
    return tuple(time)


def separate_download():
    while True:
        url = input("请输入视频链接或vid编号:")
        vid = tangdou.get_vid(url)
        if vid is None:
            print("请输入包含vid参数的视频链接或直接输入vid编号！")
        else:
            td = tangdou.VideoAPI()
            try:
                video_info = td.get_video_info(vid)
            except (ValueError, RuntimeError) as e:
                print(e)
                print("请重试！")
                continue
            else:  # Successfully obtained video information
                break
    
    urls_dict = video_info["urls"]
    if not bool(urls_dict):
            raise RuntimeError("URL列表为空！")
    print("检测到以下可选清晰度：")
    urls_list = list(enumerate(urls_dict))
    for url in urls_list:
        print(f"[{url[0]}] {url[1]}")
    while True:
        index = input("请选择需要下载的清晰度(默认为全部下载):").replace("，", ",").split(",")
        selected_urls = dict()
        if index == ['']:
            selected_urls = urls_dict.copy()
            break
        else:
            for i in index:
                i = str(i)
                if i.isdigit():
                    i = int(i)
                    if i >= len(urls_list):
                        print(f"序号 '{i}' 不存在，请重新输入！")
                        break
                    selected_urls[urls_list[i][1]] = urls_dict[urls_list[i][1]]
                else:
                    print("请输入清晰度序号，多选以逗号分隔！")
                    break
            else:
                break

    path = input("请输入文件储存目录(默认为当前目录):")
    if path == "":
        path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "Download")
    if not os.path.exists(path):  # Create the directory if it does not exist
        os.mkdir(path)
    for clarity,url in selected_urls.items():
        name = video_info["name"] + "_" + clarity
        downloader(name, url, path)

        filepath = os.path.join(path, name + ".mp4")
        video = VideoFileClip(filepath)

        while True:
            clip_start = input("剪辑起始时间(默认为不剪辑):")
            if clip_start == "":  # Do not clip
                break

            clip_start = time_check(clip_start)
            if clip_start is not None:
                break
            print("时间格式有误，请重新输入！")

        if clip_start != "":
            while True:
                clip_end = time_check(input("剪辑截止时间:"))
                if clip_end is not None:
                    break
                print("时间格式有误，请重新输入！")

            print("[%02d:%02d:%02d<--->%02d:%02d:%02d]" % (*clip_start, *clip_end))
            print(clip_start)
            video = video.subclip(clip_start, clip_end)

            while True:
                save = input("是否保存剪辑过的视频（y/n）:")
                if save == "y" or save == "n":
                    break
                print("输入有误，请重新输入！")

            if save == "y":
                filepath = os.path.join(path, name + "_clip.mp4")
                video.write_videofile(filepath)
                if not os.path.exists(filepath):
                    raise OSError("video save error, {} does not exist".format(filepath))

        while True:
            convert = input("是否转换为音频（y/n）:")
            if convert == "y" or convert == "n":
                break
            print("输入有误，请重新输入！")

        if convert == "y":
            audio = video.audio
            filepath = os.path.join(path, name + ".mp3")
            audio.write_audiofile(filepath)
            if not os.path.exists(filepath):
                raise OSError("audio save error, {} does not exist".format(filepath))


def download_video(q: Queue):
    while True:
        video_info = q.get()
        vid = video_info.pop("vid")
        try:
            name = video_info["name"]
            urls = video_info["urls"]
            path = video_info["path"]
            hd = list(urls)[0]          # Download highest definition
            name = name + "_" + hd
            url = urls[hd]
            downloader(name, url, path)
        except Exception as e:
            print(f"exception: {e}")
            print(f"{vid} {video_info['name']}.mp4 下载失败！")
        q.task_done()

download_queue = Queue()

def batch_download(json_dir, max_threads=5):
    global download_queue
    path = input("请输入文件储存目录(默认为当前目录):")
    if path == "":
        path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "Download")
    if not os.path.exists(path):  # Create the directory if it does not exist
        os.mkdir(path)
    vid_set = get_vid_set(json_dir)
    td = tangdou.VideoAPI()
    download_queue = Queue()
    for _ in range(max_threads):  # Use 5 threads
        t = threading.Thread(target=download_video, args=(download_queue,))
        t.daemon = True
        t.start()
    for vid in vid_set:
        try:
            video_info = td.get_video_info(vid)
            video_info["path"] = path
            video_info["vid"] = vid
            download_queue.put(video_info)
        except (ValueError, RuntimeError) as e:
            print(e)
            print(f"vid: {vid} 下载失败！")
            continue
    download_queue.join()

def signal_handler(signal, frame):
    global download_queue
    if not download_queue.empty() or downloading:
        while True:
            batch = input("下载尚未完成是否强制退出（y/n）:")
            if batch == "y" or batch == "n":
                break
            print("输入有误，请重新输入！")
        if batch == "n":
            return
    print("\n========================= 下载结束 =========================")
    time.sleep(2)
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

if __name__ == "__main__":
    print("===================糖豆视频下载器 By CCBP===================")
    print("     使用回车键（Enter）选择默认值，使用Ctrl+C退出程序")
    print('             清晰度选择以","、"，"作为分隔符')
    print('视频剪辑的时间输入以" "、"."、":"、"："、","、"，"作为分隔符')
    print("============================================================")
    json_dir = "DownloadList"
    if os.path.exists(json_dir):
        if os.listdir(json_dir):
            while True:
                batch = input("检测到批量下载目录非空是否尝试批量下载（y/n）:")
                if batch == "y" or batch == "n":
                    break
                print("输入有误，请重新输入！")
            if batch == "y":
                batch_download(json_dir)

    while True:
        separate_download()
