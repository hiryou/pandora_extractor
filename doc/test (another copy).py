#!/usr/bin/python

__author__ = ('Sundar Srinivasan')

import re
import sys
import urllib2

def getVideoUrl(content):
    fmtre = re.search('(?<=url_encoded_fmt_stream_map=).*', content)
    grps = fmtre.group(0).split('&amp;')
    vurls = urllib2.unquote(grps[0])
    temp = vurls.split('|')
    print temp[0]
    exit(1)
    videoUrl = None
    for vurl in vurls.split('|'):
        if vurl.find('itag=5') > 0:
            return vurl
    return None

def getTitle(content):
    title = content.split('</title>', 1)[0].split('<title>')[1]
    return sanitizeTitle(title)

def sanitizeTitle(rawtitle):
    rawtitle = urllib2.unquote(rawtitle)
    lines = rawtitle.split('\n')
    title = ''
    for line in lines:
        san = unicode(re.sub('[^\w\s-]', '', line).strip())
        san = re.sub('[-\s]+', '_', san)
        title = title + san
    ffr = title[:4]
    title = title[5:].split(ffr, 1)[0]
    return title

def downloadVideo(f, resp):
    totalSize = int(resp.info().getheader('Content-Length').strip())
    currentSize = 0
    CHUNK_SIZE = 32768

    while True:
        data = resp.read(CHUNK_SIZE)

        if not data:
            break
        currentSize += len(data)
        f.write(data)

        print('============> ' + \
                  str(round(float(currentSize*100)/totalSize, 2)) + \
                  '% of ' + str(totalSize) + ' bytes')
        if currentSize >= totalSize:
            break
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python youtap.py \"<youtube-url>\"")
        exit(1)
    urlname = sys.argv[1].split('&', 1)[0]
    print('Downloading: ' + urlname)
    try: 
        resp = urllib2.urlopen(urlname)
    except urllib2.HTTPError:
        print('Bad URL: 404')
        exit(1)
    content = resp.read()
    videoUrl = getVideoUrl(content)
    ## videoUrl = 'http://r6---sn-nx57yn7d.c.youtube.com/videoplayback?ms=au&itag=5&expire=1359994725&mv=m&source=youtube&sver=3&factor=1.25&mt=1359969256&sparams=algorithm%2Cburst%2Ccp%2Cfactor%2Cid%2Cip%2Cipbits%2Citag%2Csource%2Cupn%2Cexpire&cp=U0hUTllUUl9HT0NONF9RTlZIOlEya19Vejdzam1W&upn=J26x4H2ZwSM&ip=67.189.123.183&newshard=yes&algorithm=throttle-factor&burst=40&key=yt1&id=bf120e509edbcba5&fexp=906076%2C919361%2C911305%2C916612%2C920704%2C912806%2C922403%2C922405%2C929901%2C913605%2C925710%2C920201%2C913302%2C930101%2C919009%2C911116%2C926403%2C910221%2C901451%2C919114&ipbits=8&title=Electric%20Daisy%20Violin-%20Lindsey%20Stirling%20%28Original%20Song%29&signature=575906F6A082A9038CC642E105C49B9E5D9C3972.7411A43A655207439D7DF26265D29E965136382A'
    if not videoUrl:
        print('Video URL cannot be found')
        exit(1)
    title = getTitle(content)
    filename = title + '.flv'
    print('Creating file: ' + filename)
    f = open(filename, 'wb')
    print('Download begins...')

    ## Download video
    video = urllib2.urlopen(videoUrl)
    downloadVideo(f, video)
    f.flush()
    f.close()
