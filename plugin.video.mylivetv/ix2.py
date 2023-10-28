import six
from six.moves.urllib.parse import urljoin, unquote_plus, quote_plus, quote, unquote
from resources.modules import control, client
import re
import xbmc
import xbmcplugin
import common
import xbmcgui
Dialog = xbmcgui.Dialog()

ix2_url = 'https://2ix2.com/'

headers = {'User-Agent': client.agent(),
           'Referer': ix2_url}

def get_lists(url):
    data = client.request(ix2_url)
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    channels = client.parseDOM(data, 'div', attrs={'class': 'sidebar-right'})
    channels = client.parseDOM(channels, 'li')
    for channel in channels:
        channelurl = client.parseDOM(channel, 'a', ret='href')[0]
        channelname = client.parseDOM(channel, 'a')[0]
        common.addDir(channelname, channelurl, 20,
           common.ICON, common.FANART, channelname)

def get_channels(url):
    data = client.request(url)
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    channels = client.parseDOM(data, 'div', attrs={'class': 'moviefilm'})
    for channel in channels:
        imgurl = client.parseDOM(channel, 'img', ret='src')[0]
        channelname = client.parseDOM(channel, 'img', ret='alt')[0]
        channelurl = client.parseDOM(channel, 'a', ret='href')[0]
        common.addDir(channelname, channelurl, 21,
           imgurl, common.FANART, channelname)
        #xbmc.log('@#@EDATAAA: {} - {} - {}'.format(text,sporturl, imgurl))
        
def get_stream(url):  # 18
    #xbmc.log('@#@DATAAAA: {}'.format(url))
    data = client.request(url)
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    data = client.parseDOM(data, 'div', attrs={'class': 'filmcontent'})
    name = client.parseDOM(data, 'a', ret="title")[0]
    script = client.parseDOM(data, 'script', attrs={'type': 'text/javascript'})[0]
    m3u8=re.sub(r'.*file: "([^"]*)",.*', r'\1', script, flags=re.DOTALL)
    xbmc.log('M3U8: {}'.format(m3u8), xbmc.LOGINFO)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'poster': 'poster.png', 'banner': 'banner.png'})
    liz.setArt({'icon': common.iconimage, 'thumb': common.iconimage, 'poster': common.iconimage, 'fanart': common.fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty("IsPlayable", "true")
    liz.setPath(str(m3u8))
    if float(xbmc.getInfoLabel('System.BuildVersion')[0:4]) >= 17.5:
        liz.setMimeType('application/vnd.apple.mpegurl')
        liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
        # liz.setProperty('inputstream.adaptive.stream_headers', str(headers))
    else:
        liz.setProperty('inputstreamaddon', None)
        liz.setContentLookup(True)
    xbmc.Player().play(m3u8, liz, False)
    quit()