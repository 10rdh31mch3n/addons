# -*- coding: utf-8 -*-
try:
    import debug
except:
    pass
import base64
import re
import sys
import six
from six.moves.urllib.parse import urljoin, unquote_plus, quote_plus, quote, unquote
from six.moves import zip
import json
import xbmc
import xbmcgui
import xbmcplugin
from resources.modules import control, client
import livetv
import common
import ix2

Dialog = xbmcgui.Dialog()

from dateutil.parser import parse
from dateutil.tz import gettz
from dateutil.tz import tzlocal

# reload(sys)
# sys.setdefaultencoding("utf-8")

#######################################
# Time and Date Helpers
#######################################
try:
    local_tzinfo = tzlocal()
    locale_timezone = json.loads(xbmc.executeJSONRPC(
        '{"jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "locale.timezone"}, "id": 1}'))
    if locale_timezone['result']['value']:
        local_tzinfo = gettz(locale_timezone['result']['value'])
except:
    pass

def convDateUtil(timestring, newfrmt='default', in_zone='UTC'):
    if newfrmt == 'default':
        newfrmt = xbmc.getRegion('time').replace(':%S', '')
    try:
        in_time = parse(timestring)
        in_time_with_timezone = in_time.replace(tzinfo=gettz(in_zone))
        local_time = in_time_with_timezone.astimezone(local_tzinfo)
        return local_time.strftime(newfrmt)
    except:
        return timestring


def Main_menu():
    common.addDir('[B][COLOR gold]Live TV SX[/COLOR][/B]', livetv.livetv_url, 16, common.ICON, common.FANART, '')
    common.addDir('[B][COLOR gold]2ix2[/COLOR][/B]', ix2.ix2_url, 19, common.ICON, common.FANART, '')
    
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmcplugin.setContent(int(sys.argv[1]), 'videos')

def idle():
    if float(xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')[:4]) > 17.6:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    else:
        xbmc.executebuiltin('Dialog.Close(busydialog)')


def busy():
    if float(xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')[:4]) > 17.6:
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    else:
        xbmc.executebuiltin('ActivateWindow(busydialog)')




def Open_settings():
    control.openSettings()

print(str(common.ADDON_PATH) + ': ' + str(common.VERSION))
print("Mode: " + str(common.mode))
print("URL: " + str(common.url))
print("Name: " + str(common.name))
print("IconImage: " + str(common.iconimage))
#########################################################

if common.mode == None:
    Main_menu()
elif common.mode == 16:
    livetv.get_livetv_sports(common.url)
elif common.mode == 17:
    livetv.get_livetv_events(common.url)
elif common.mode == 18:
    livetv.get_livetv_stream(common.url)

elif common.mode == 19:
    ix2.get_lists(common.url)
elif common.mode == 20:
    ix2.get_channels(common.url)
elif common.mode == 21:
    ix2.get_stream(common.url)
    
elif common.mode == 100:
    livetv.resolve(common.url, common.name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
