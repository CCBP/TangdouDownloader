# 糖豆视频下载器

![Python](https://img.shields.io/badge/Python-3.8.3-red)
![Author](https://img.shields.io/badge/Author-CCBP-blue)
![license](https://img.shields.io/badge/license-MIT-lightgrey)
<img src="https://www.ccbp.me/wp-content/uploads/2022/05/b812aff8b32a9412aa5247b0ff14889c.jpg" alt="banner">

# 使用说明

在[发布页面](https://github.com/CCBP/TangdouDownloader/releases/)下载打包编译好的可执行程序后便可直接双击运行，由于本人时间有限并没有为其编写图形界面，故运行会会显示命令窗口，通过在窗口中根据提示进行交互即可。

🔴**目前仅支持视频所使用的音乐音频下载**，因为通过下面所说的两种视频原始连接获取方法得到的连接中包含`sign`参数，怀疑是因为此参数不正确，导致无论是任何`vid`，得到的都是名为`hello.mp4`的视频，**如果对此您有任何可能的解决方法，欢迎联系我**。

# 实现方法

[糖豆](https://www.tangdoucdn.com/)视频都是以URL的参数`vid`作为引索，可以通过`vid`获得想要的视频。原始视频链接的获取有HTML解析与API接口请求两种方式。

## 视频API请求

上面所说的访问`www.tangdoucdn.com/h5/play?vid=`无法找到`video`标签，是因为这个连接下的页面中的`video`标签是动态生成的，而其生成的方式正式通过访问它的API接口获取的原始视频链接，接口地址为`api-h5.tangdou.com/sample/share/main?vid=`。

该接口返回一个JSON格式数据，对该数据进行解析后`data`属性下的`video_url`的值正是原始视频链接，`title`属性的值则为使用Unicode编码的视频名称，但要想从此接口正常获取数据需提供请求标头如下：
```
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh,zh-CN;q=0.9
Connection: keep-alive
Host: api-h5.tangdou.com
Referer: https://www.tangdoucdn.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36
```

## 音频API请求

糖豆提供了音频的API，可以直接获得此视频中所使用的歌曲音频（不带教学），接口地址为`api-h5.tangdou.com/sample/share/recommend?page_num=1&vid=`。

该接口返回一个JSON格式数据，对该数据进行解析后`data`属性的值为一个**数组**，数组的第二列中的`mp3url`的值为原始音频链接，`title`属性的值为使用Unicode编码的音频名称，所需请求标头同上。

## HTML解析

通过访问视频链接，通过GET方法获得响应体，响应体为HTML文档，对其进行解析寻找`video`标签便可获得视频原始连接。但若直接访问`www.tangdoucdn.com/h5/play?vid=`是无法找到`video`标签的，而是要访问`share.tangdou.com/splay.php?vid=`才可以。

# 关于打包
这里我使用的是`pyinstaller`对程序打包为`exe`文件，但直接使用命令`pyinstaller -F -i assets/icon/download.ico main.py`进行打包并运行后会出现`FileNotFound`错误，提示`matplotlibrc`无法找到。

在搜索到[Python Pyinstaller Matplotlibrc](https://stackoverflow.com/questions/62701684/python-pyinstaller-matplotlibrc)、[Pyinstaller adding data files](https://stackoverflow.com/questions/41870727/pyinstaller-adding-data-files)与[Finding the rc configuration file](https://www.oreilly.com/library/view/matplotlib-for-python/9781788625173/901d6e2a-5bb4-44f5-bbba-dabef1a0df40.xhtml)后将，`matplotlibrc`文件复制到与程序同一目录下，使用命令`pyinstaller -F --add-data "matplotlibrc;." -i assets/icon/download.ico  main.py`进行打包即可消除此错误。

以及对`moviepy`打包时出现如下问题：
```
AttributeError: module ‘moviepy.video.fx.all’ has no attribute ‘crop’
AttributeError: module ‘moviepy.audio.fx.all’ has no attribute ‘audio_fadein’
```
参照[moviepy用pyinstaller打包问题](https://blog.csdn.net/CaRrrCa/article/details/109269055)即可解决。

ps: Python打包真是太麻烦了，不只麻烦，打包出来的东西因为依赖的关系有非常大，想缩减又是很麻烦。

# 致谢
<a href="https://www.flaticon.com/free-icons/direct-download" title="direct download icons">Direct download icons created by Freepik - Flaticon</a>

# 音频API
请求网址: https://api-h5.tangdou.com/sample/share/recommend?page_num=1&vid=20000002326426&new_rec=1&openid=td_e6e91cdfd15708590dc38fae5b1ae5f6
请求方法: GET
状态代码: 200 OK
远程地址: 117.50.84.168:443
引荐来源网址政策: strict-origin-when-cross-origin