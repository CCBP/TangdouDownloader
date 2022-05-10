import json
import requests
from headers import headers
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class HTML(object):
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

class API(object):
    '''
    Obtain the original video connection by accessing the API interface and 
    parsing the returned JSON data
    '''

    def __init__(self):
        self.url = 'http://api-h5.tangdou.com/sample/share/main?vid='
        self.state = False

    def get_api_info(self, vid):
        '''use vid to get video information through api interface
        :param vid: video id in the url, must be a string of numbers
        :param return: return a dict that include the video information 
        if the request is successful, otherwise throw an RuntimeError
        '''
        vid = str(vid)
        if not vid.isdigit():  # vid must a string of numbers
            raise TypeError('vid should be a string of numbers not', 
                            type(vid), vid)

        header = headers(self.url).buildHeader()
        resp = requests.get(self.url + vid, headers=header)
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            raise RuntimeError('request error, error code:', resp.status_code)

    def get_video_info(self, url):
        '''use vid to get video spicific information
        :param url: video url that containing vid or just vid 
        :param return: return a dict that include video title and video original address
        '''
        url = str(url)
        if url.isdigit():   # just vid
            vid = url
        else:
            query = urlparse(url).query
            params = parse_qs(query)
            if 'vid' in params:
                vid = params['vid'][0]
            else:
                raise ValueError("can not find 'vid' parameter from '{}'".format(url))
        
        api_dict = self.get_api_info(vid)

        video_info = dict()
        video_info['title'] = api_dict['data']['title']
        video_info['addr'] = api_dict['data']['video_url']

        return video_info
        
