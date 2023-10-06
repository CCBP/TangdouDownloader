# 糖豆视频下载器

![Python](https://img.shields.io/badge/Python-3.8.3-red)
![Author](https://img.shields.io/badge/Author-CCBP-blue)
![license](https://img.shields.io/badge/license-MIT-lightgrey)
<img src="https://www.amrzs.net/wp-content/uploads/2022/05/b812aff8b32a9412aa5247b0ff14889c.jpg" alt="banner">

# 使用说明

在[发布页面](https://github.com/CCBP/TangdouDownloader/releases/)下载最新版本的应用程序后便可直接双击 `tangdou_video.exe` 运行。由于本人时间有限并没有为其编写图形界面，故运行会会显示命令窗口，通过在窗口中根据提示进行交互即可。

使用过程中需要注意的是：

- 需要提供想要下载的视频链接，链接中必须包含 vid 参数，或者也可以直接输入 vid 编号；
- 使用回车键（Enter）选择默认值；
- 由于使用单线程下载，故下载速度可能并不会很快；
- 会在选择的储存目录下自动生成 Download 文件夹，之后所有的文件都将储存至该文件夹；
- 若想要下载的视频已经存在则不会再次下载；
- 若需要进行视频剪辑则需要输入起始与结束时间，时、分、秒之间可以使用” “(空格)、”.“(英文句号)、”:“(英文冒号)、”:“(中文冒号)、”,“(英文逗号)、”，“(中文逗号) 进行分隔，以上分隔符也可以混用（不推荐），时、分、秒若高位为 0 也可不全部给出，合法的输入示例如下（以 0 时 2 分 30 秒为例）：
  - 0:2:30
  - 2:30
  - 0.2.30
  - 2 30
  - 0.2:30(不推荐)
- 可以选择不进行剪辑，无论是否进行剪辑都可以在之后的提示中选择将视频文件转换为音频文件；
- 剪辑过的视频可以选择不保存，无论是否选择保存都可以在之后的提示中选择将视频文件转换为音频文件；
- 使用 Ctrl+C 可随时结束程序。

运行应用后会打印出简单的使用提示，示例交互过程如下：
```
===================糖豆视频下载器 By CCBP===================
     使用回车键（Enter）选择默认值，使用Ctrl+C退出程序
视频剪辑的时间输入以" "、"."、":"、"："、","、"，"作为分隔符
============================================================
请输入视频链接或vid编号:https://www.tangdoucdn.com/h5/play?vid=20000002258422&utm_campaign=client_share&utm_source=tangdou_android&utm_medium=wx_chat&utm_type=0&share_uid=#1652176249257
请输入文件储存目录(默认为当前目录):
[308.71 s] Download completed, save to d:\Workspace\Python\tangdou\Download\安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学.mp4 
剪辑起始时间(默认为不剪辑):2.30
剪辑截止时间:5.0
是否保存剪辑过的视频（y/n）:y
[00:02:30<--->00:05:00]
Moviepy - Building video d:\Workspace\Python\tangdou\Download\安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学_edited.mp4.
MoviePy - Writing audio in 安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学_editedTEMP_MPY_wvf_snd.mp3
MoviePy - Done.
Moviepy - Writing video d:\Workspace\Python\tangdou\Download\安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学_edited.mp4
 
Moviepy - Done !
Moviepy - video ready d:\Workspace\Python\tangdou\Download\安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学_edited.mp4
是否转换为音频（y/n）:y
MoviePy - Writing audio in d:\Workspace\Python\tangdou\Download\安徽金社《母亲》网红一夜火爆最新男生版 母亲节献礼附教学.mp3
MoviePy - Done.
请输入视频链接或vid编号:https://www.tangdoucdn.com/h5/play?vid=20000002258422&utm_campaign=client_share&utm_source=tangdou_android&utm_medium=wx_chat&utm_type=0&share_uid=#1652176249257
请输入文件储存目录(默认为当前目录):
[11.35 s] Download completed, save to D:\Workspace\Python\tangdou\dist\Download\雨凡《疯疯疯》64步弹跳附分解.mp4
剪辑起始时间(默认为不剪辑):11
剪辑截止时间:3.56
是否保存剪辑过的视频（y/n）:n
是否转换为音频（y/n）:y
MoviePy - Writing audio in D:\Workspace\Python\tangdou\dist\Download\雨凡《疯疯疯》64步弹跳附分解.mp3
MoviePy - Done.
请输入视频链接或vid编号:Traceback (most recent call last):
  File "d:\Workspace\Python\tangdou\main.py", line 144, in <module>
    main()
  File "d:\Workspace\Python\tangdou\main.py", line 62, in main
    url = input('请输入视频链接或vid编号:')
KeyboardInterrupt
```

> Linux 用户可以自行安装 python 以及使用 `pip install -r requirement.txt` 安装依赖，执行命令 `python main.py` 运行程序

> 支持批量下载糖豆视频，可通过抓包获取喜欢、收藏、下载的请求结果，将响应体保存至 `input` 文件中，程序会自动解析文件中的请求结果并下载视频。

# 实现方法

[糖豆](https://www.tangdoucdn.com/)视频都是以URL的参数`vid`作为引索，可以通过`vid`获得想要的视频。原始视频链接的获取有HTML解析与API接口请求两种方式。

## 视频API请求

接口地址为`api-h5.tangdou.com/sample/share/main?vid=`，该接口返回一个JSON格式数据，对该数据进行解析后`data`属性下的`video_url`的值正是原始视频链接，`title`属性的值则为使用Unicode编码的视频名称，但要想从此接口正常获取数据需提供请求标头如下：

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

糖豆视频页面下方会有推荐的**相关视频**，接口地址为`api-h5.tangdou.com/sample/share/recommend?page_num=1&vid=`。该接口返回一个JSON格式数据，对该数据进行解析后`data`属性的值为一个**数组**，数组的每一个元素即为一个推荐的视频，其中的`mp3url`的值为原始音频链接，`title`属性的值为使用Unicode编码的音频名称，所需请求标头同上。

其中`mp3url`的值为`https://mp3qingiu.tangdou.com/wuqu/xxxx.mp3`，直接通过该地址即可获取音频文件，但`xxxx.mp3`为一个长度为32的编号，通过观察推断该编号为使用MD5算法生成的，由于不清楚原文是什么，故无法直接使用该链接地址获取音频。

🔴此接口实际上为获取视频下方**推荐视频**对应的音频，并不是我们实际想要的音频，故暂时**弃用**此方法。

## HTML解析

通过访问视频链接，通过GET方法获得响应体，响应体为HTML文档，对其进行解析寻找`video`标签便可获得视频原始连接。但若直接访问`www.tangdoucdn.com/h5/play?vid=`是无法找到`video`标签的，因为该地址中的`video`标签为动态生成的。而访问`share.tangdou.com/splay.php?vid=`则可以直接获取`video`标签。

> 通过对视频原始链接的分析，可以发现视频链接中存在 `{vid}_H360P` 关键字，其中 `{vid}` 为视频编号， `H360P` 为视频清晰度，通过修改 `H360P` 的值可以获取不同清晰度的视频，目前发现了存在 `H720P`, `V720P`, `H540P`, `H360P` , 但为了避免错过可能存在的清晰度等级，代码中按照 `level = ["H1080P", "V1080P", "H720P", "V720P", "H540P", "V540P", "H360P", "V360P"]` 遍历请求的。

> 遍历多个清晰度视频链接并不会对速度有多大影响，因为 `404` 响应的速度很快。

## 注意

下载时必须附带如下请求头才可正常获取我们想要的视频：

```
Referer: https://www.tangdoucdn.com
```

否则下载到的视频则是一个名为`hello.mp4`的默认视频文件。

# 关于打包

## pyinstaller

这里我使用的是`pyinstaller`对程序打包为`exe`文件，但直接使用命令`pyinstaller -F -i assets/icon/download.ico main.py`进行打包并运行后会出现`FileNotFound`错误，提示`matplotlibrc`无法找到。

在搜索到[Python Pyinstaller Matplotlibrc](https://stackoverflow.com/questions/62701684/python-pyinstaller-matplotlibrc)、[Pyinstaller adding data files](https://stackoverflow.com/questions/41870727/pyinstaller-adding-data-files)与[Finding the rc configuration file](https://www.oreilly.com/library/view/matplotlib-for-python/9781788625173/901d6e2a-5bb4-44f5-bbba-dabef1a0df40.xhtml)后将，`matplotlibrc`文件复制到与程序同一目录下，使用命令`pyinstaller -F --add-data "matplotlibrc;." -i assets/icon/download.ico  main.py`进行打包即可消除此错误。

以及对`moviepy`打包时出现如下问题：

```
AttributeError: module ‘moviepy.video.fx.all’ has no attribute ‘crop’
AttributeError: module ‘moviepy.audio.fx.all’ has no attribute ‘audio_fadein’
```
参照[moviepy用pyinstaller打包问题](https://blog.csdn.net/CaRrrCa/article/details/109269055)即可解决。

ps: Python打包真是太麻烦了，不只麻烦，打包出来的东西因为依赖的关系有非常大，想缩减又是很麻烦。

## python embedded

由于使用`pyinstaller`打包出来的exe文件体积过大不利于传播，并且程序的启动加载速度也过于缓慢。并且为了使用户无需自主配置python环境，因此通过添加嵌入式python环境的方式执行程序，教程参考知乎文章[pyinstaller打包的exe太大？你需要嵌入式python玄学](https://zhuanlan.zhihu.com/p/77028265)。

# 致谢

<a href="https://www.flaticon.com/free-icons/direct-download" title="direct download icons">Direct download icons created by Freepik - Flaticon</a>
