echo id ICON "assets/icon/download.ico" > ico.rc
windres -i ico.rc -o ico.o
gcc main.c ico.o -o tangdou_video.exe
del ico.rc ico.o