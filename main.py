import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tangdou, time, requests, re
from moviepy.editor import *
from headers import headers

def downloader(name, url, path):
    if not os.path.exists(path):
        raise ValueError("'{}' does not exist".format(path))
    start = time.time()                                     # Download start
    header = headers(url).buildHeader()
    response = requests.get(url, headers=header, stream=True)
    size = 0                                                # Downloaded file size
    chunk_size = 1024                                       # data size per download
    content_size = int(response.headers['content-length'])  # Total download file size
    if response.status_code == 200:                         # Download succesful
        filepath = os.path.join(path, name + '.mp4')
        with open(filepath, 'wb') as file:                  # Show prograss bar
            for data in response.iter_content(chunk_size = chunk_size):
                print('\rtotal:{size:.2f} MB'.format(
                        size = content_size / chunk_size / 1024
                    ), end='', flush=True)
                file.write(data)
                size += len(data)
                percentage = size / content_size
                print(' |%s%s| %.2f%%' % (
                        '▆' * int(percentage * 100), 
                        ' ' * (100 - int(percentage * 100)),
                        float(size / content_size * 100)
                    ), end='', flush=True)
        end = time.time()                                   # Download completed
        if os.path.exists(filepath):
            print('\r[%.2f s] Download completed, save to %s' % 
                    (end - start, os.path.abspath(filepath)))
        else:
            raise OSError('Download error, {} does not exist'.format(filepath))
    else:
        raise RuntimeError('request error, error code:', response.status_code)

def time_check(time_str):
    '''convert time string to tuple and check its format
    :param str: the time string with ' ', '.', ':', '：', ',' and '，' as delimiter
    :param return: return a tuple that looks like (hour, minute, second) if the 
    input format is correct, otherwise return None
    '''
    splitted = re.split(' |\.|:|：|,|，', time_str)
    if len(splitted) > 3:
        return None

    time = [0, 0, 0]
    limit = (60, 60, 24)        # Reversed
    splitted.reverse()          # Reverse order traversal
    for i in range(len(splitted)):
        tmp = splitted[i]
        if tmp.isdigit() and int(tmp) < limit[i]:
            time[i] = int(tmp)
        else:
            return None

    time.reverse()
    return tuple(time)

def main():
    while True:
        url = input('请输入视频链接或vid编号:')
        vid = tangdou.get_vid(url)
        if vid is None:
            print("请输入包含vid参数的视频链接或直接输入vid编号！")
        else:
            td = tangdou.VideoAPI()
            try:
                video_info = td.get_video_info(vid)
            except (ValueError, RuntimeError) as e:
                print(e)
                print('请重试！')
                continue
            else:                   # Successfully obtained video information
                break

    path = input('请输入文件储存目录(默认为当前目录):')
    if path == '':
        path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'Download')
    if not os.path.exists(path):    # Create the directory if it does not exist
         os.mkdir(path)
    video_info['path'] = path
    filepath =  os.path.join(video_info['path'], video_info['name'] + '.mp4')
    if os.path.exists(filepath):
        print(filepath, '已存在！')
    else:
        downloader(**video_info)    # Unfold this dict to pass parameters

    video = VideoFileClip(filepath)

    while True:
        clip_start = input('剪辑起始时间(默认为不剪辑):')
        if clip_start == '':        # Do not clip
            break

        clip_start = time_check(clip_start)
        if clip_start is not None:
            break
        print('时间格式有误，请重新输入！')

    if (clip_start != ''):
        while True:
            clip_end = time_check(input('剪辑截止时间:'))
            if clip_end is not None:
                break
            print('时间格式有误，请重新输入！')

        print('[%02d:%02d:%02d<--->%02d:%02d:%02d]' % (*clip_start, *clip_end))
        print(clip_start)
        video = video.subclip(clip_start, clip_end)

        while True:
            save = input('是否保存剪辑过的视频（y/n）:')
            if save == 'y' or save == 'n':
                break
            print('输入有误，请重新输入！')

        if save == 'y':
            filepath = os.path.join(video_info['path'], video_info['name'] + '_clip.mp4')
            video.write_videofile(filepath)
            if not os.path.exists(filepath):
                raise OSError('video save error, {} does not exist'.format(filepath))

    while True:
        convert = input('是否转换为音频（y/n）:')
        if convert == 'y' or convert == 'n':
            break
        print('输入有误，请重新输入！')

    if convert == 'y':
        audio = video.audio
        filepath = os.path.join(video_info['path'], video_info['name'] + '.mp3')
        audio.write_audiofile(filepath)
        if not os.path.exists(filepath):
            raise OSError('audio save error, {} does not exist'.format(filepath))

if __name__ == '__main__':
    print('===================糖豆视频下载器 By CCBP===================')
    print('     使用回车键（Enter）选择默认值，使用Ctrl+C退出程序')
    print('视频剪辑的时间输入以" "、"."、":"、"："、","、"，"作为分隔符')
    print('============================================================')
    while True:
        main()
