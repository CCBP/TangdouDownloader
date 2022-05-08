# 糖豆视频下载器

[糖豆](https://www.tangdoucdn.com/)视频都是以URL的参数`vid`作为引索，可以通过`vid`获得想要的视频。原始视频链接的获取有HTML解析与API接口请求两种方式。

# HTML解析

通过访问视频链接，通过GET方法获得响应体，响应体为HTML文档，对其进行解析寻找`video`标签便可获得视频原始连接。但若直接访问`www.tangdoucdn.com/h5/play?vid=`是无法找到`video`标签的，而是要访问`share.tangdou.com/splay.php?vid=`才可以。

# API接口请求

上面所说的访问`www.tangdoucdn.com/h5/play?vid=`无法找到`video`标签，是因为这个连接下的页面中的`video`标签是动态生成的，而其生成的方式正式通过访问它的API接口获取的原始视频链接，接口地址为`api-h5.tangdou.com/sample/share/main?vid=`。该接口返回一个JSON格式数据，对该数据进行解析后`data`属性下的`video_url`的值正是原始视频链接，但要想从此接口正常获取数据需提供请求标头如下：
```
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh,zh-CN;q=0.9
Connection: keep-alive
Host: api-h5.tangdou.com
Referer: https://www.tangdoucdn.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36
```
由于使用API接口更加统一，故此下载器使用API接口的方式获取原始视频链接。