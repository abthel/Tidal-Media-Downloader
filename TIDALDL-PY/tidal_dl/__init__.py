# -*- coding: utf-8 -*-
import sys
import os

from aigpy import pipHelper
from aigpy import pathHelper
from aigpy.cmdHelper import myinput,myinputInt

import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount
from tidal_dl.download import Download
from tidal_dl.printhelper import printMenu,printChoice2,printErr

TIDAL_DL_VERSION = "2019.7.25.0"

def logIn(username = "", password = ""):
    if username == "" or password == "":
        print("----------------LogIn------------------")
        username = myinput("username:")
        password = myinput("password:")
    account  = TidalAccount(username, password)
    account2 = TidalAccount(username, password,True)
    if account.errmsg != "":
        printErr(0, account.errmsg)
        return False
    if account2.errmsg != "":
        printErr(0, account2.errmsg)
        return False

    cf = TidalConfig()
    cf.set_account(username, password, account.session_id, account.country_code, account.user_id, account2.session_id)
    return True


def setting():
    cf = TidalConfig()
    print("----------------Setting----------------")
    print("OutputDir    :\t" + cf.outputdir)
    print("SoundQuality :\t" + cf.quality)
    print("Resolution   :\t" + cf.resolution)
    print("ThreadNum    :\t" + cf.threadnum)
    while True:
        outputdir = myinput("Outputdir(Enter '0' Unchanged):".ljust(12))
        if outputdir == '0':
            outputdir = cf.outputdir
            break
        if os.path.isdir(outputdir) == False:
            printErr(0, "Path is Err!")
            continue
        break
    while True:
        index = myinputInt("Quality(0-LOW,1-HIGH,2-LOSSLESS,3-HI_RES):".ljust(12), 999)
        if index > 3 or index < 0:
            printErr(0, "Quality Err!")
            continue
        if index == 0:
            quality = 'LOW'
        if index == 1:
            quality = 'HIGH'
        if index == 2:
            quality = 'LOSSLESS'
        if index == 3:
            quality = 'HI_RES'
        break
    while True:
        index = myinputInt("Resolution(0-1080,1-720,2-480,3-360,4-240):".ljust(12),99)
        if index > 4 or index < 0:
            printErr(0, "ThreadNum Err")
            continue
        if index == 0:
            resolution = '1080'
        if index == 1:
            resolution = '720'
        if index == 2:
            resolution = '480'
        if index == 3:
            resolution = '360'
        if index == 4:
            resolution = '240'
        break
    while True:
        threadnum = myinput("ThreadNum:".ljust(12))
        if cf.valid_threadnum(threadnum) == False:
            printErr(0, "ThreadNum Err")
            continue
        break

    cf.set_outputdir(outputdir)
    cf.set_quality(quality)
    cf.set_resolution(resolution)
    cf.set_threadnum(threadnum)

    pathHelper.mkdirs(outputdir + "/Album/")
    pathHelper.mkdirs(outputdir + "/Playlist/")
    pathHelper.mkdirs(outputdir + "/Video/")
    pathHelper.mkdirs(outputdir + "/Favorite/")
    return

def main(argv=None):
    cf = TidalConfig()
    dl = Download()
    print(tidal.LOG)
    while logIn(cf.username, cf.password) == False:
        pass

    onlineVer = pipHelper.getLastVersion('tidal-dl')
    print("====================Tidal-dl========================")
    print("Username     :\t" + cf.username)
    print("OutputDir    :\t" + cf.outputdir)
    print("SessionID    :\t" + cf.sessionid)
    print("CountryCode  :\t" + cf.countrycode)
    print("SoundQuality :\t" + cf.quality)
    print("Resolution   :\t" + cf.resolution)
    print("ThreadNum    :\t" + cf.threadnum)
    print("Version      :\t" + TIDAL_DL_VERSION)
    if onlineVer != None:
        print("LastVer      :\t" + onlineVer)
    print("====================================================")
    while True:
        printMenu()
        strchoice,choice = printChoice2("Enter Choice:", 99)
        if choice == 0:
            return
        elif choice == 1:
            logIn()
            dl = Download(cf.threadnum)
        elif choice == 2:
            setting()
            dl = Download(cf.threadnum)
        elif choice == 3:
            dl.downloadAlbum()
        elif choice == 4:
            dl.downloadTrack()
        elif choice == 5:
            dl.downloadPlaylist()
        elif choice == 6:
            dl.downloadVideo()
        elif choice == 7:
            dl.downloadFavorite()
        elif choice == 8:
            dl.downloadArtistAlbum()
        else:
            dl.downloadUrl(strchoice)

def debug():
    # cf = TidalConfig()
    # while logIn(cf.username, cf.password) == False:
    #     pass
# add tag Credits,Info song and full tag (discnumber,irsc,composer,arrenger,publisher,replayGain,releasedate)
# https://api.tidal.com/v1/albums/71121869/tracks?token=wdgaB1CilGA-S_s2&countryCode=TH


    dl = Download()
    dl.downloadAlbum(91166670)
    # dl.downloadVideo(57261945) #1hours
    # dl.downloadVideo(92418079)
# if __name__ == '__main__':
#     main(sys.argv)

__all__ = ['main', 'tidal', 'download']
