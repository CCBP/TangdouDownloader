import tangdou, os, time, requests

def downloader(name, url, path):
    if not os.path.exists(path):
        raise ValueError("'{}' does not exist".format(path))
    start = time.time()                                     # Download start
    response = requests.get(url, stream=True)
    size = 0                                                # Downloaded file size
    chunk_size = 1024                                       # data size per download
    content_size = int(response.headers['content-length'])  # Total download file size
    if response.status_code == 200:                         # Download succesful
        filepath = path + '\\' + name + '.mp3'
        with open(filepath, 'wb') as file:                  # Show prograss bar
            for data in response.iter_content(chunk_size = chunk_size):
                print('\rtotal:{size:.2f} MB'.format(
                        size = content_size / chunk_size / 1024
                    ), end='', flush=True)
                file.write(data)
                size += len(data)
                percentage = size / content_size
                print(' |%s%s| %.2f%%' % (
                        '▆' * int(percentage * 50), 
                        ' ' * (50 - int(percentage * 50)),
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

def main():
    while True:
        url = input('请输入音频链接或vid编号:')
        vid = tangdou.get_vid(url)
        if vid is None:
            print("请输入包含vid参数的音频链接或直接输入vid编号！")
        else:
            td = tangdou.AudioAPI()
            try:
                audio_info = td.get_audio_info(vid)
            except (ValueError, RuntimeError) as e:
                print(e)
                print('请重试！')
                continue
            else:                   # Successfully obtained video information
                break

    path = input('请输入文件储存目录(默认为当前目录):')
    if path == '':
        path = os.path.dirname(os.path.abspath(__file__))
    path += '\\Download'
    if not os.path.exists(path):    # Create the directory if it does not exist
         os.mkdir(path)
    audio_info['path'] = path
    filepath = audio_info['path'] + '\\' + audio_info['name'] + '.mp3'
    if os.path.exists(filepath):
        print(filepath, '已存在！')
    else:
        downloader(**audio_info)    # Unfold this dict to pass parameters

if __name__ == '__main__':
    print('===================糖豆音频下载器 By CCBP===================')
    print('     使用回车键（Enter）选择默认值，使用Ctrl+C退出程序')
    print('============================================================')
    while True:
        main()