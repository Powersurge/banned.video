#############################################################
# Project: 			#		Banned.Video Plugin
# ver. 2.1.7
# Email @ thomasmeadows@gmail.com
#############################################################
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import xbmc
import re
import os
import sys
import string
import logging
import random
import array
import time
import datetime
import json
import requests
import inputstreamhelper
import urllib.request
import urllib.parse
# import simplejson as json

IW_addon_id = "plugin.video.banned.video"
IW_domain_url = "banned.video"
IW_addonPath = os.path.join("special://home", "addons", IW_addon_id)
IW_artIcon = os.path.join(IW_addonPath, "icon.png")
IW_artFanart = os.path.join(IW_addonPath, "fanart.jpg")
IW_plugin = "Banned.Video"
IW_authors = "Prafit, Spinalcracker"
IW_credits = ""
IW_database_name = "infowars"
IW_database_file = os.path.join(
    xbmc.translatePath("special://database"), 'infowars.db')
IW_debugging = False
AJSIcon = "https://imgur.com/YYl3GFe.png"
DKSIcon = "https://assets.infowarsmedia.com/images/15084c28-71d4-456f-b587-7b66f73c7ede-large.png"
DKSFanart = "https://assets.infowarsmedia.com/images/203cf9b2-f811-4802-bfb4-441b2e864a7c-large.png"
WarRoomIcon = "https://static.infowars.com/images/war-room-logo-white.png"
WarRoomFanart = "https://static.infowars.com/images/war-room-studio.jpg"
FPIcon = "https://i.imgur.com/Nc3LAtC.png"
FPFanart = "https://i.imgur.com/VsMhpSz.jpg"
CTIcon = "https://imgur.com/XA1mZtd.png"
CTFanart = "https://imgur.com/KloueqE.jpg"
IWLiveSEIcon = "https://imgur.com/i4TqWhY.png"
IWLiveSEFanart = "https://www.infowars.com/wp-content/uploads/2018/08/jones-censored23.jpg"
PJWIcon = "https://i.imgur.com/A9R4qjv.jpg"
PJWFanart = "https://i.imgur.com/ZksTDyX.jpg"
MWIcon = "https://i.imgur.com/5KMuph0.jpg"
MWFanart = "https://www.infowarsteam.com/wp-content/uploads/2016/10/Millie-Weaver.jpg"
KBIcon = "https://imgur.com/6eHYGNi.jpg"
KBFanart = "https://imgur.com/2tv5KdN.jpg"
IWODIcon = "https://imgur.com/PcR2j1b.png"
IWODFanart = "https://i.imgur.com/40Prkn5.jpg"  # "https://imgur.com/Un7aMqX.jpg"
IWODFLSIcon = "https://imgur.com/fgVD9Ps.png"
IWBDVIcon = "https://i.imgur.com/i9YU0t9.png"

module_log_enabled = False

# Write something on XBMC log


def log(message):
    xbmc.log(message)

# Write this module messages on XBMC log


def _log(message):
    if module_log_enabled:
        xbmc.log(""+message)

# Parse string and extracts multiple matches using regular expressions


def find_multiple_matches(text, pattern):
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

# Parse string and extracts first match as a string
def find_single_match(text, pattern):
    result = ""
    try:
        matches = re.findall(pattern, text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""
    return result


def eod(): xbmcplugin.endOfDirectory(int(sys.argv[1]))


# For Coloring Text ###
def cFL(t, c="green"): return '[COLOR '+c+']' + t +'[/COLOR]'


# For Coloring Text (First Letter-Only) ###
def cFL_(t, c="green"): return '[COLOR '+c+']' + t[0:1] + '[/COLOR]' + t[1:]

def notification(header="", message="", sleep=5000): xbmc.executebuiltin(
    "XBMC.Notification(%s,%s,%i)" % (header, message, sleep))


def WhereAmI(t):  # for Writing Location Data to log file ###
    if (IW_debugging == True):
        print('Where am I:  '+t)


def deb(s, t):  # for Writing Debug Data to log file ###
    if (IW_debugging == True):
        print(s+':  '+t)


def debob(t):  # for Writing Debug Object to log file ###
    if (IW_debugging == True):
        print(t)


def nolines(t):
    it = t.splitlines()
    t = ''
    for L in it:
        t = t+L
    t = ((t.replace("\r", "")).replace("\n", ""))
    return t


def iFL(t): return '[I]'+t+'[/I]'  # For Italic Text ###


def bFL(t): return '[B]'+t+'[/B]'  # For Bold Text ###


def _FL(t, c, e=''):  # For Custom Text Tags ###
    if (e == ''):
        d = ''
    else:
        d = ' '+e
    return '['+c.upper()+d+']'+t+'[/'+c.upper()+']'


def add_item(mode="", title="", plot="", url="", icon="DefaultVideo.png", thumbnail="", fanart="", folder=True):
    listitem = xbmcgui.ListItem(title)
    listitem.setInfo("video", {"Title": title, "Plot": plot})
    listitem.setArt({"icon": icon, "thumb": thumbnail, "fanart": fanart})
    if not folder:
        listitem.setProperty('IsPlayable', 'true')

    if url.startswith("plugin://"):
        itemurl = url
    else:
        itemurl = '%s?mode=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % (sys.argv[0], mode, urllib.parse.quote_plus(title),
                    urllib.parse.quote_plus(url), urllib.parse.quote_plus(thumbnail), urllib.parse.quote_plus(plot))
    xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)


def PlayURL(url):
    listitem = xbmcgui.ListItem(path=url)

    if 'm3u8' in url.lower():
        # if it is hls, then set relevant properties
        if inputstreamhelper.Helper('hls').check_inputstream():
            listitem.setProperty('inputstream', 'inputstream.adaptive')
            listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


def ToTop():
    wnd = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    id = wnd.getFocusId()
    xbmc.executebuiltin('SetFocus(id, 1)')


def Menu_MainMenu():  # The Main Menu
    add_item(
        mode='PlayURL',
        title=cFL_('The Alex Jones Show - (Loops After Airing)', 'lime'),
        url='https://freespeech.akamaized.net/hls/live/2024573/live2/playlist.m3u8',
        icon=AJSIcon, thumbnail=AJSIcon, fanart=IW_artFanart,
        folder=False
    )
    add_item(
        mode='PlayURL',
        title=cFL_('The American Journal with Harrison Smith - (Loops After Airing)', 'orange'),
        url='https://freespeech.akamaized.net/hls/live/2016873/live3/playlist.m3u8',
        icon=DKSIcon, thumbnail=DKSIcon, fanart=DKSFanart,
        folder=False
    )
    add_item(
        mode='PlayURL',
        title=cFL_('War Room with Owen Shroyer - (Loops After Airing)', 'purple'),
        url='https://freespeech.akamaized.net/hls/live/2024574/live4/playlist.m3u8',
        icon=WarRoomIcon, thumbnail=WarRoomIcon, fanart=WarRoomFanart,
        folder=False
    )
    # # IW_addon.add_directory({'mode': 'PlayURL','url':''},{'title':  cFL_('American Countdown - (Loops After Airing)','red')},is_folder=False,img=IWODIcon,fanart=IWODFanart)
    add_item(
        mode='PlayURL',
        title=cFL_('Live Shows & Special Events', 'green'),
        url='https://freespeech.akamaized.net/hls/live/2016712/live1/playlist.m3u8',
        icon=IWLiveSEIcon, thumbnail=IWLiveSEIcon, fanart=IWLiveSEFanart,
        folder=False
    )
    add_item(
        mode='AJShowArchiveSubMenu',
        title=cFL_('On Demand Videos (Banned.video)', 'cyan'),
        icon=IWODIcon, thumbnail=IWODIcon, fanart=IWODFanart,
        folder=True
    )
    add_item(
        mode='PaulJosephWatsonSubMenu',
        title=cFL_('Paul Joseph Watson (Youtube)', 'blue'),
        icon=PJWIcon, thumbnail=PJWIcon, fanart=PJWFanart,
        folder=True
    )
    add_item(
        mode='MillieWeaverSubMenu',
        title=cFL_('Millie Weaver (Youtube)', 'pink'),
        icon=MWIcon, thumbnail=MWIcon, fanart=MWFanart,
        folder=True
    )
    add_item(
        mode='KaitlinBennettSubMenu',
        title=cFL_('Kaitlin Bennett - Liberty Hangout (Youtube)', 'yellow'),
        icon=KBIcon, thumbnail=KBIcon, fanart=KBFanart,
        folder=True
    )
    add_item(
        mode='GregReeseSubMenu',
        title=cFL_('Greg Reese - InfoWars (Youtube)', 'green'),
        icon=IWODIcon, thumbnail=IWODIcon, fanart=IWODFanart,
        folder=True
    )
    add_item(
        mode='JonBowneReportsSubMenu',
        title=cFL_('Jon Bowne Reports - InfoWars (Youtube)', 'purple'),
        icon=IWODIcon, thumbnail=IWODIcon, fanart=IWODFanart,
        folder=True
    )

    eod()


def Paul_Joseph_Watson_Sub_Menu(title=''):
    # https://www.youtube.com/user/PrisonPlanetLive
    WhereAmI('@ Paul Joseph Watson')
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCittVh8imKanO_5KohzDbpg'
    response = urllib.request.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read().decode(response.headers.get_content_charset())
        videos = find_multiple_matches(content, "<entry>(.*?)</entry>")
        for entry in videos:
            title = find_single_match(entry, "<titl[^>]+>([^<]+)</title>")
            plot = find_single_match(
                entry, "<media\:descriptio[^>]+>([^<]+)</media\:description>")
            thumbnail = find_single_match(
                entry, "<media\:thumbnail url=\"(.*?)\"")
            video_id = find_single_match(
                entry, "<yt\:videoId>([^<]+)</yt\:videoId>")
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    else:
        util.showError(
            ADDON_ID, 'Could not open URL %s to create menu' % (url))

    eod()


def Millie_Weaver_Sub_Menu(title=''):
    # https://www.youtube.com/channel/UCglVbeKF9JGMCt-RTUAW_TQ
    WhereAmI('@ Millie Weaver')
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCglVbeKF9JGMCt-RTUAW_TQ'
    response = urllib.request.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read().decode(response.headers.get_content_charset())
        videos = find_multiple_matches(content, "<entry>(.*?)</entry>")
        for entry in videos:
            title = find_single_match(entry, "<titl[^>]+>([^<]+)</title>")
            plot = find_single_match(
                entry, "<media\:descriptio[^>]+>([^<]+)</media\:description>")
            thumbnail = find_single_match(
                entry, "<media\:thumbnail url=\"(.*?)\"")
            video_id = find_single_match(
                entry, "<yt\:videoId>([^<]+)</yt\:videoId>")
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    else:
        util.showError(
            ADDON_ID, 'Could not open URL %s to create menu' % (url))

    eod()


def Kaitlin_Bennett_Sub_Menu(title=''):
    # https://www.youtube.com/channel/UCglVbeKF9JGMCt-RTUAW_TQ
    WhereAmI('@ Millie Weaver')
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCQMb7c66tJ7Si8IrWHOgAPg'
    response = urllib.request.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read().decode(response.headers.get_content_charset())
        videos = find_multiple_matches(content, "<entry>(.*?)</entry>")
        for entry in videos:
            title = find_single_match(entry, "<titl[^>]+>([^<]+)</title>")
            plot = find_single_match(
                entry, "<media\:descriptio[^>]+>([^<]+)</media\:description>")
            thumbnail = find_single_match(
                entry, "<media\:thumbnail url=\"(.*?)\"")
            video_id = find_single_match(
                entry, "<yt\:videoId>([^<]+)</yt\:videoId>")
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    else:
        util.showError(
            ADDON_ID, 'Could not open URL %s to create menu' % (url))

    eod()


def Greg_Reese_Sub_Menu(title=''):
    # https://www.youtube.com/channel/UCoZXzeOEtomauxdqLbRlAew
    WhereAmI('@ Millie Weaver')
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCoZXzeOEtomauxdqLbRlAew'
    response = urllib.request.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read().decode(response.headers.get_content_charset())
        videos = find_multiple_matches(content, "<entry>(.*?)</entry>")
        for entry in videos:
            title = find_single_match(entry, "<titl[^>]+>([^<]+)</title>")
            plot = find_single_match(
                entry, "<media\:descriptio[^>]+>([^<]+)</media\:description>")
            thumbnail = find_single_match(
                entry, "<media\:thumbnail url=\"(.*?)\"")
            video_id = find_single_match(
                entry, "<yt\:videoId>([^<]+)</yt\:videoId>")
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    else:
        util.showError(
            ADDON_ID, 'Could not open URL %s to create menu' % (url))

    eod()


def Jon_Bowne_Reports_Sub_Menu(title=''):
    # https://www.youtube.com/channel/UC3P0x8HufuxSNkOiH-25ODQ
    WhereAmI('@ Millie Weaver')
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC3P0x8HufuxSNkOiH-25ODQ'
    response = urllib.request.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read().decode(response.headers.get_content_charset())
        videos = find_multiple_matches(content, "<entry>(.*?)</entry>")
        for entry in videos:
            title = find_single_match(entry, "<titl[^>]+>([^<]+)</title>")
            plot = find_single_match(
                entry, "<media\:descriptio[^>]+>([^<]+)</media\:description>")
            thumbnail = find_single_match(
                entry, "<media\:thumbnail url=\"(.*?)\"")
            video_id = find_single_match(
                entry, "<yt\:videoId>([^<]+)</yt\:videoId>")
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    else:
        util.showError(
            ADDON_ID, 'Could not open URL %s to create menu' % (url))

    eod()


def aj_search(iw, titleCheck):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    data = None
    tc = titleCheck
    url = 'https://api.infowarsmedia.com/graphql/'
    id = "5b9429906a1af769bc31efeb"
    new_id = iw
    query = """query IFWGetChannelVideos($id: String!="%s", $limit: Float=15, $offset: Float=0)
    { getChannel(id: $id)
    {videos(limit: $limit, offset: $offset)
    { _id title summary playCount largeImage embedUrl directUrl published videoDuration channel
    { _id title avatar}
    }
    }
    }"""
    # print query
    req = requests.post(url, json={'query': query % (new_id)}, headers=hdr)

    type(req)

    len(req.text)
    aj = json.loads(req.text)
    try:
        for a in aj["data"]["getChannel"]["videos"]:
            # print i
            # print (i["title"].encode("utf-8"),i["summary"],i["largeImage"],i["directUrl"])
            plot = a["summary"].encode("utf-8")
            thumbnail = a["largeImage"]
            video_id = a["directUrl"]
            title = tc + " - " + a["title"]
            url = video_id
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)
    except:
        print("Error")


def Full_Show_Sub_Menu(title=''):
    WhereAmI('@ Recent Full Length Shows')
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    urlBannedVideo = 'https://banned.video'
    idBV = ""

    dataBV = None
    reqBV = urllib.request.Request(urlBannedVideo, dataBV, hdr)
    # responseBV = urllib2.urlopen(reqBV)
    # contentBV = responseBV.read()
    idBV = ["5b885d33e6646a0015a6fa2d", "5b9301172abf762e22bc22fd", "5b92d71e03deea35a4c6cdef", "5d7a86b1f30956001545dd71", "5d7faa8432b5da0013fa65bd", "5da504e060be810013cf7252", "5d8d03dbd018a5001776876a", "5da8c506da090400138c8a6a",
            "5dbb4729ae9e840012c61293", "5d9653676f2d2a00179b8a58", "5b9429906a1af769bc31efeb", "5d7fa9014ffcfc00130304fa", "5cf7df690a17850012626701", "5dae2e7f612f0a0012d147bf", "5ec2e150244ac5001d2a6486", "5f444e76df77c4044ef6adbc", "5e4d5777071ff9001c065ce0"]
    # idBV = (find_multiple_matches(contentBV,"<a href=\"\/channel\/(.*?)\""))  *** Save for future switch to javascript dynamic handling ***
    urlMAIN = 'https://api.infowarsmedia.com/api/channel/'
    # IW_addon.log('*******  ' + urlMAIN)
    for i in range(len(idBV)):
        dataMAIN = None
        urlMAINID = urlMAIN + str(idBV[i]).strip('[\']') + '/'
        # IW_addon.log('*******  ' + urlMAINID)
        reqMAIN = urllib.request.Request(urlMAINID, dataMAIN, hdr)
        responseMAIN = urllib.request.urlopen(reqMAIN)
        dataMAIN = json.load(responseMAIN)

        titleCheck = dataMAIN["title"]

        url = urlMAINID + 'videos/'

        data = None
        import requests
        try:
            req = requests.get(url=url, data=data, headers=hdr)

        # req = urllib2.Request(url, data ,hdr)
        # response = urllib2.urlopen(req)
            type(req)
            len(req.text)

            data = json.loads(req.text)

            item = data["featuredVideo"]
            title = titleCheck + " - " + item["title"]
            plot = item["summary"]
            thumbnail = item["posterThumbnailUrl"]
            video_id = item["directUrl"]
            url = video_id
            # if ("FULL" in title or "Full" in title) and ("SHOW" in title or "Show" in title):
            add_item(mode="PlayURL", title=title, plot=plot,
                     url=url, thumbnail=thumbnail, folder=False)

        except:
            print("Error")

    eod()


def Alex_Jones_Show_Archive_Sub_Menu(title=''):
    # https://www.infowars.com/videos/
    add_item(
        mode='ToTop',
        title=cFL('         ===== Welcome to Banned.video =====', 'cyan'),
        icon=IWBDVIcon, thumbnail=IWBDVIcon, fanart=IWODFanart,
        folder=True
    )
    add_item(
        mode='FullShowSubMenu',
        title=cFL('===[ Click Here For Recent Full Length Shows ]===', 'red'),
        icon=IWODFLSIcon, thumbnail=IWODFLSIcon, fanart=IWODFanart,
        folder=True
    )

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    urlBannedVideo = 'https://banned.video'
    idBV = ""

    dataBV = None
    # reqBV = urllib2.Request(urlBannedVideo, dataBV, hdr)
    # responseBV = urllib2.urlopen(reqBV)
    # contentBV = responseBV.read()
    idBV = ["5b885d33e6646a0015a6fa2d", "5b9301172abf762e22bc22fd", "5b92d71e03deea35a4c6cdef", "5d7a86b1f30956001545dd71", "5d7faa8432b5da0013fa65bd", "5da504e060be810013cf7252", "5d8d03dbd018a5001776876a", "5da8c506da090400138c8a6a", "5dbb4729ae9e840012c61293",
            "5d9653676f2d2a00179b8a58", "5b9429906a1af769bc31efeb", "5d7fa9014ffcfc00130304fa", "5cf7df690a17850012626701", "5dae2e7f612f0a0012d147bf", "5ebad3ff244ac5001d2134ff", "5e822d4115f81d009d49b580", "5ec2e150244ac5001d2a6486", "5f444e76df77c4044ef6adbc", "5e4d5777071ff9001c065ce0"]
    # idBV = (find_multiple_matches(contentBV,"<a href=\"\/channel\/(.*?)\""))
    urlMAIN = 'https://api.infowarsmedia.com/api/channel/'
    for i in range(len(idBV)):
        dataMAIN = None
        urlMAINID = urlMAIN + str(idBV[i]).strip('[\']') + '/'
        reqMAIN = urllib.request.Request(urlMAINID, dataMAIN, hdr)
        responseMAIN = urllib.request.urlopen(reqMAIN)
        dataMAIN = json.load(responseMAIN)

        titleCheck = dataMAIN["title"]

        url = urlMAINID + 'videos/'
        import requests
        data = None
        # req = urllib2.Request(url, data ,hdr)
        iw = idBV[i]

        try:
            req = requests.get(url=url, data=data, headers=hdr)
            # response = urllib2.urlopen(req)
            # type(req)
            # len(req.text)
            # data = json.load(response)
            data = json.loads(req.text)
            item = data["featuredVideo"]
            title = titleCheck + " - " + item["title"]
            plot = item["summary"].encode("utf-8")
            thumbnail = item["posterThumbnailUrl"]
            video_id = item["directUrl"]
            url = video_id

            ############ new search ###############
            if not "Full Show" in title:
                aj_search(iw, titleCheck)
        except:
            print("Error")
            aj_search(iw, titleCheck)

    add_item(
        mode='ToTop',
        title=cFL('===[ Click Here To Return To Top ]===', 'grey'),
        icon=IWODIcon, thumbnail=IWODIcon, fanart=IWODFanart,
        folder=True
    )

    eod()


def check_mode(mode=''):
    args = urllib.parse.parse_qs(sys.argv[2][1:])
    mode = None
    url = ''
    title = ''
    thumbnail = ''

    if 'mode' in args:
        mode = args.get('mode')[0]
    if 'url' in args:
        url = args.get('url')[0]
    if 'title' in args:
        title = args.get('title')[0]
    if 'thumbnail' in args:
        thumbnail = args.get('thumbnail')[0]

    # if mode:
    #     print("Mode = "+mode)

    if (mode == '') or (mode == 'main') or (mode == 'MainMenu'):
        Menu_MainMenu()  # Default Menu
    elif (mode == 'PlayURL'):
        PlayURL(url)  # Play Video
    elif (mode == 'ToTop'):
        ToTop()
    elif (mode == 'PaulJosephWatsonSubMenu'):
        Paul_Joseph_Watson_Sub_Menu(title)
    elif (mode == 'MillieWeaverSubMenu'):
        Millie_Weaver_Sub_Menu(title)
    elif (mode == 'KaitlinBennettSubMenu'):
        Kaitlin_Bennett_Sub_Menu(title)
    elif (mode == 'GregReeseSubMenu'):
        Greg_Reese_Sub_Menu(title)
    elif (mode == 'JonBowneReportsSubMenu'):
        Jon_Bowne_Reports_Sub_Menu(title)
    elif (mode == 'AJShowArchiveSubMenu'):
        Alex_Jones_Show_Archive_Sub_Menu(title)
    elif (mode == 'FullShowSubMenu'):
        Full_Show_Sub_Menu(title)
    else:
        # So that if a mode isn't found, it'll goto the Main Menu and give you a message about it.
        Menu_MainMenu()


# Runs the function that checks the mode and decides what the plugin should do. This should be at or near the end of the file.
check_mode()
