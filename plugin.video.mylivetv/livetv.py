import six
from six.moves.urllib.parse import urljoin, unquote_plus, quote_plus, quote, unquote
from resources.modules import control, client
import re
import xbmc
import xbmcplugin
import common
import xbmcgui
Dialog = xbmcgui.Dialog()

livetv_url = 'https://livetv.ru/'

headers = {'User-Agent': client.agent(),
           'Referer': livetv_url}

def get_livetv_sports(url):
    purl='{}/enx/allupcomingsports/'
    data = client.request(purl.format(url, 1))
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    data = client.parseDOM(data, 'table', attrs={'cellpadding': '0', 'cellspacing': '0', 'height': '27', 'width': '94%', 'background': 'cdn.livetv719.me/img/sbgg2.gif', 'style': 'background-position: right;'})
    common.addDir('[B][COLOR white]{}[/COLOR][/B]'.format('TOP Events Live'), purl.format(url), 17, '', common.FANART, 'TOP Events Live')
    for sport in data:
        imgtd = client.parseDOM(sport, 'td', attrs={'background': '//cdn.livetv719.me/img/sbggg.gif', 'width': '27'})[0]
        imgurl = 'http:{}'.format(client.parseDOM(imgtd, 'img', ret='src')[0])
        texttd = client.parseDOM(sport, 'td')[0]
        text = client.parseDOM(texttd, 'b')[0]
        sporturl = client.parseDOM(texttd, 'a', ret='href')[0]
        common.addDir('[B][COLOR white]{}[/COLOR][/B]'.format(text), url + sporturl, 17,
           imgurl, common.FANART, text)
        #xbmc.log('@#@EDATAAA: {} - {} - {}'.format(text,sporturl, imgurl))

def parse_event(event):
    tds = client.parseDOM(event, 'td')
    name = client.replaceHTMLCodes(client.parseDOM(tds, 'a')[0])
    islive = len(client.parseDOM(tds, 'img', attrs={'src': '//cdn.livetv719.me/img/live.gif'})) == 1
    eventurl = '{}{}'.format(livetv_url, client.parseDOM(tds, 'a', ret='href')[0])
    timespan=client.parseDOM(tds, 'span', attrs={'class': 'evdesc'})[0].strip()
    eventtime = re.sub('\r.*', '', timespan, flags=re.DOTALL)
    xbmc.log('@#@EDATAAA: {} - {} - {}'.format(name, eventurl, eventtime))
    tds = client.parseDOM(event, 'td', attrs={'valign': 'top'})
    comp = client.parseDOM(tds, 'img', ret="alt")[0]
    imgurl = 'https:{}'.format(client.parseDOM(tds, 'img', ret="src")[0])
    watch = '[COLORlime]*[/COLOR]' if islive else '[COLORred]*[/COLOR]'
    ftime = '[COLORcyan]{}[/COLOR]'.format(eventtime)
    return (watch, ftime, name, comp, imgurl, eventurl)

def get_livetv_events(url):
    xbmc.log('@#@EDATAAA: {}'.format(url))
    data = client.request(url)
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    if re.compile(r'.*[0-9]/$').match(url):
        data = client.parseDOM(data, 'table', attrs={'class': 'main'})[0]
    else:
        data = client.parseDOM(data, 'span', attrs={'id': 'upcoming'})[0]
    data = client.parseDOM(data, 'table', attrs={'width': '100%', 'cellpadding': '1', 'cellspacing': '2'})
    xbmc.log('@#@EDATAAA: {}'.format(data))
    for event in data:
        (watch, ftime, name, comp, imgurl, eventurl) = parse_event(event)
        common.addDir('{} {} {} [I]{}[/I]'.format(watch, ftime, name, comp), eventurl, 18, imgurl, common.FANART, name)

def get_livetv_stream(url):  # 18
    #xbmc.log('@#@DATAAAA: {}'.format(url))
    data = client.request(url)
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    acestreams = client.parseDOM(data, 'td', attrs={'width': '220'})
    webstreams = client.parseDOM(data, 'td', attrs={'width': '227'})
    weblinks = client.parseDOM(str(webstreams), 'td', attrs={'width': '15'})
    weblinks = client.parseDOM(str(weblinks), 'a', ret='href')
    acelinks = client.parseDOM(str(acestreams), 'td', attrs={'width': '15'})
    acelinks = client.parseDOM(str(acelinks), 'a', ret="href")
    #xbmc.log('@#@STREAMMMMMSSSSSS:%s' % weblinks, xbmc.LOGINFO)
    titles = []
    streams = []
    weblinks=list(zip(client.parseDOM(str(webstreams), 'img', attrs={'width': '16'}, ret='title'), client.parseDOM(client.parseDOM(str(webstreams), 'td', attrs={'width': '15'}), 'a', ret='href')))
    acelinks=list(zip(client.parseDOM(str(acestreams), 'img', attrs={'width': '16'}, ret='title'), client.parseDOM(client.parseDOM(str(acestreams), 'td', attrs={'width': '15'}), 'a', ret='href')))

    for lang, link in weblinks:
        if 'alieztv' in link:
            streams.append('https:{}'.format(link.rstrip()))
            titles.append('{} {}'.format(lang, len(titles)+1))

    for lang, link in acelinks:
            streams.append(link.rstrip())
            titles.append('ACE {} {}'.format(lang, len(titles)+1))

    if len(streams) > 1:
        dialog = xbmcgui.Dialog()
        ret = dialog.select('[COLORgold][B]Choose Stream[/B][/COLOR]', titles)
        if ret == -1:
            return
        elif ret > -1:
            host = streams[ret]
            xbmc.log('@#@STREAMMMMM:%s' % host)
            return resolve(host, common.name)
        else:
            return False
    else:
        link = streams[0]
        return resolve(link, common.name)

def get_livetv(url):
    data = client.request(url)
    # xbmc.log('@#@EDATAAA: {}'.format(data))
    data = six.ensure_text(data, encoding='utf-8', errors='ignore')
    data = client.parseDOM(data, 'table', attrs={'class': 'styled-table'})[0]
    chans = list(zip(client.parseDOM(data, 'button', attrs={'class': 'tvch'}),
                    client.parseDOM(data, 'a', ret='href')))
    for chan, stream in chans:
        # stream = str(quote(base64.b64encode(six.ensure_binary(stream))))

        chan = chan.encode('utf-8') if six.PY2 else chan
        chan = '[COLOR gold][B]{}[/COLOR][/B]'.format(chan)

        common.addDir(chan, stream, 100, common.ICON, common.FANART, common.name)

def resolve(url, name):
    ragnaru = ['liveon.sx/embed', '//em.bedsport', 'cdnz.one/ch', 'cdn1.link/ch', 'cdn2.link/ch']
    xbmc.log('RESOLVE-URL: %s' % url, xbmc.LOGINFO)
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    ua = 'Mozilla/5.0 (iPad; CPU OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1'
    # dialog.notification(AddonTitle, '[COLOR skyblue]Attempting To Resolve Link Now[/COLOR]', icon, 5000)
    if re.compile(r'.*cdn.livetv[0-9]{3}.me.*').match(url):
        html = client.request(url, referer=livetv_url)
        html = six.ensure_text(html, encoding='utf-8', errors='ignore')
        iframeurl = 'https:{}'.format(re.sub(r'\s', '', client.parseDOM(html, 'iframe', attrs={'scrolling': 'no'}, ret='src')[0].strip()))
        html = client.request(iframeurl, referer=url)
        html = six.ensure_text(html, encoding='utf-8', errors='ignore')
        script=client.parseDOM(html, 'script')
        script=script[len(script)-1]
        m3u8='https:{}'.format(re.sub(r".*pl.init\('(.*)'\).*", r'\1', script, flags=re.DOTALL))
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
    if 'acestream' in url:
        url1 = "plugin://program.plexus/?url=" + url + "&mode=1&name=acestream+"
        liz = xbmcgui.ListItem(name)
        liz.setArt({'poster': 'poster.png', 'banner': 'banner.png'})
        liz.setArt({'icon': common.iconimage, 'thumb': common.iconimage, 'poster': common.iconimage,
                    'fanart': common.fanart})
        liz.setPath(url)
        xbmc.Player().play(url1, liz, False)
        quit()