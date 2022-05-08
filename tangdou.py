# author: gorquan <gorquanwu@gmail.com>
# date: 2019.8.15

import requests
from headers import headers
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class tangdou(object):
    """获取糖豆广场舞视频类
    :param object: object
    """
    def __init__(self,url):
        """tangdou class init
        :param self: self
        :param url: 视频页面地址
        """
        self.headers = None
        self.url = url
        self.videoUrl = None
        self.success = False

    def __getvideoUrl(self):
        """解析网页获取视频地址
        :param self: self
        """   
        urlResp = requests.get(self.url, headers=self.headers)
        urlResp.encoding = urlResp.apparent_encoding
        if urlResp.status_code == 200:
            print(urlResp.text)
            page = BeautifulSoup(urlResp.text, 'lxml')
            self.videoUrl = (page.find('video')).get('src')
            self.success = True
        else:
            self.videoUrl = None

    def getVideoUrl(self):
        """获取视频地址
        :param self: self
        :param return: 返回视频地址videoUrl和解析状态success
        """   
        self.headers = headers(self.url).buildHeader()
        self.__getvideoUrl()
        return {'success': self.success, 'videoUrl': self.videoUrl}
