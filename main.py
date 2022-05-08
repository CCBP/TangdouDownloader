import tangdou

url = input('tangdou url:')
td = tangdou.tangdou(url)
print(td.getVideoUrl())