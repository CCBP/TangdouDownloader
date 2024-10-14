import json, requests, re
from headers import headers
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_vid(url):
    '''Parse the url to get the vid parameter
    :param url: tangdou video url that containing vid or just vid 
    :param return: return the vid parameter if parsing is successful, 
    otherwise return None
    '''
    vid = None
    url = str(url)
    if url.isdigit():   # just vid
        vid = url
    else:
        query = urlparse(url).query
        params = parse_qs(query)
        if 'vid' in params:
            vid = params['vid'][0]

    return vid

class HTML(object):
    '''
    Obtain the original video address by visiting the parsing HTML page 
    and looking for the video tag
    '''

    def __init__(self):
        self.url = 'http://share.tangdou.com/splay.php?vid='

    def get_video_url(self, url):
        '''parse the webpage to get the video address
        :param url: tangdou video url that containing vid or just vid 
        :param return: 
        '''
        vid = get_vid(url)
        if vid is None:
            raise ValueError("can not find 'vid' parameter from '{}'".format(url))

        header = headers(self.url).buildHeader()
        resp = requests.get(self.url + vid, headers=header)
        resp.encoding = resp.apparent_encoding
        if resp.status_code == 200:
            page = BeautifulSoup(resp.text, 'lxml')
            return (page.find('video')).get('src')  # original video address
        else:
            raise RuntimeError('request error, error code:', resp.status_code)

class VideoAPI(object):
    '''
    Obtain the original video address by accessing the API interface and 
    parsing the returned JSON data
    '''

    def __init__(self):
        self.url = 'http://api-h5.tangdou.com/sample/share/main?vid='

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
        :param url: tangdou video url that containing vid or just vid 
        :param return: return a dict that include video title and video original address
        '''
        vid = get_vid(url)
        if vid is None:
            raise ValueError("can not find 'vid' parameter from '{}'".format(url))
        
        api_dict = self.get_api_info(vid)

        video_info = dict()
        video_info['name'] = api_dict['data']['title']
        urls = dict()
        video_info['urls'] = urls
        
        # Get a list of video URLs in different definitions
        url = api_dict['data']['video_url']
        clarity = ('H1080P', 'V1080P', 'H720P', 'V720P', 'H540P', 'V540P', 'H360P', 'V360P')
        header = headers(url).buildHeader()

        if re.search('_.[0-9]+P', url):
            for c in clarity:
                urls[c] = re.sub('_.[0-9]+P', f'_{c}', url)
        else:
            urls['unknown'] = url

        for key in urls.copy().keys():
            response = requests.get(urls[key], headers=header, stream=True)
            if response.status_code == 404:
                urls.pop(key, None)
        return video_info

class AudioAPI(object):

    def __init__(self):
        self.url = 'https://api-h5.tangdou.com/sample/share/recommend?page_num=1&vid='

    def get_api_info(self, vid):
        '''use vid to get video information through api interface
        :param vid: audio id in the url, must be a string of numbers
        :param return: return a dict that include the audio information 
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

    def get_audio_info(self, url):
        '''use vid to get audio spicific information
        :param url: tangdou audio url that containing vid or just vid 
        :param return: return a dict that include audio title and audio original address
        '''
        vid = get_vid(url)
        if vid is None:
            raise ValueError("can not find 'vid' parameter from '{}'".format(url))
        
        api_dict = self.get_api_info(vid)

        audio_info = dict()
        audio_info['name'] = api_dict['data'][1]['title']
        audio_info['url'] = api_dict['data'][1]['mp3url']

        return audio_info