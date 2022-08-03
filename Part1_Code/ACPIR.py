import pymysql
import win32evtlog  # requires pywin32 pre-installed
import os
import sys
import ctypes
import winreg
import datetime
import string
import binascii
import struct
import subprocess
import collections
import uuid
import msvcrt
import time
import wmi
import socket
import json
from traceback import print_tb
import olefile
from sqlalchemy import false, true
from pathlib import Path
import win32security
from sqlalchemy import create_engine
import pandas as pd
import io
import hashlib
import ntpath
import tempfile
import re
import sqlite3

msp21074_logo=('''********************************************************************

          _          ______   _______    _____   _______      
         / \       .' ___  | |_   __ \  |_   _| |_   __ \    
        / _ \     / .'   \_|   | |__) |   | |     | |__) |   
       / ___ \    | |          |  ___/    | |     |  __ /    
      / / _ \ \_  \ `.___.'\  _| |_      _| |_   _| |  \ \_  
    |____| |____|  `.____ .' |_____|    |_____| |____| |___| 
                                                         

********************************************************************

[Copyright @ HKUCS Msp21074, Artifacts Collector & Parser For IR]''')

# Accurate to minute
from datetime import datetime as dt
collect_time = dt.now().strftime('%Y%m%d%H%M%S')

def GetMAC():
    MAC = uuid.UUID(int=uuid.getnode()).hex[-12:]
    MAC="-".join([MAC[e:e + 2] for e in range(0, 11, 2)]).upper()
    return MAC

#################################################################################################
############################################################################################
# This part of the code refers to https://github.com/salehmuhaysin/JumpList_Lnk_Parser
# this class is define for jumplist and lnk
class JL:
    codecs = ["ascii","utf-8"]
    def __init__(self):
        self.quiet=True
        self.pretty=True
        self.output_format = 'csv'#    = args.output_format if args.output_format is not None and args.output_format in ['json' , 'csv'] else 'json'
        self.delimiter =',' #      = args.delimiter if args.delimiter is not None else ','
        self.output_file_lnk = 'lnk_parsed.csv'  #  = args.output_file if args.output_file is not None else None
        self.output_file_jumplist ='jumplist_parsed.csv'
        # define the appids, for parse the jumplist files
        AppIDs={'12dc1ea8e34b5a6': ('Application IDs', 'Microsoft Paint 6.1'), '17d3eb086439f0d7': ('Application IDs', 'TrueCrypt 7.0a'), '18434d518c3a61eb': ('Application IDs', 'Minitab 17'), '1b4dd67f29cb1962': ('Application IDs', 'Windows Explorer Pinned and Recent.'), '1bc392b8e104a00e': ('Application IDs', 'Remote Desktop'), '23646679aaccfae0': ('Image/Document Viewers', 'Adobe Acrobat 9.4.0'), '26717493b25aa6e1': ('Application IDs', 'Adobe Dreamweaver CS5 (32-bit)'), '271e609288e1210a': ('Application IDs', 'Microsoft Office Access 2010 x86'), '28c8b86deab549a1': ('Internet Browsers', 'Internet Explorer 8 / 9'), '290532160612e071': ('Utilities', 'WinRAR 2.90 / 3.60 / 4.01'), '2b53c4ddf69195fc': ('Application IDs', 'Zune x64'), '3094cdb43bf5e9c2': ('Application IDs', 'Microsoft Office OneNote 2010 x86'), '315e29a36e961336': ('Application IDs', 'Roboform 7.8'), '40f2aca05d8a33f2': ('Application IDs', 'Minitab 16'), '431a5b43435cc60b': ('Application IDs', 'Python (.pyc)'), '43578521d78096c6': ('Application IDs', 'Windows Media Player Classic Home Cinema 1.3 (32-bit)'), '44a3621b32122d64': ('Application IDs', 'Microsoft Office Word 2010 x64'), '44a398496acc926d': ('Application IDs', 'Adobe Premiere Pro CS5 (64-bit)'), '469e4a7982cea4d4': ('Application IDs', 'Windows Wordpad'), '500b8c1d5302fc9c': ('Application IDs', 'Python (.pyw)'), '50620fe75ee0093': ('Application IDs', 'VMware Player 3.1.4'), '550abc1cb58eb92c': ('Application IDs', 'VeraCrypt 1.16 / 1.19 64-bit'), '590aee7bdd69b59b': ('Application IDs', 'Powershell Windows 10'), '5c450709f7ae4396': ('Internet Browsers', 'Firefox 1.0 / 2.0 / 3.0'), '5d6f13ed567aa2da': ('Application IDs', 'Microsoft Office Outlook 2010 x64'),
'5da8f997fd5f9428': ('Application IDs', 'Internet Explorer x64'), '5f6e7bc0fb699772': ('Application IDs', 'Microsoft Office PowerPoint 2010 x64'), '65009083bfa6a094': ('Application IDs', '(app launched via XPMode)'), '6728dd69a3088f97': ('Application IDs', 'Windows Command Processor - cmd.exe (64-bit)'), '6d2bac8f1edf6668': ('Application IDs', 'Microsoft Office Outlook 365'), '6e855c85de07bc6a': ('Application IDs', 'Microsoft Office Excel 2010 x64'), '74d7f43c1561fc1e': ('Media Players', 'Windows Media Player 12.0.7601.17514'), '7e4dca80246863e3': ('Application IDs', 'Control Panel (?)'), '83b03b46dcd30a0e': ('Media Players', 'iTunes 9.0.0.70 / 9.2.1.5 / 10.4.1.10 (begin custom â€˜Tasksâ€™ JL capability)'), '84f066768a22cc4f': ('Application IDs', 'Adobe Photoshop CS5 (64-bit)'), '89b0d939f117f75c': ('Application IDs', 'Adobe Acrobat 9 Pro Extended (32-bit)'), '8eafbd04ec8631ce': ('Application IDs', 'VMware Workstation 9 x64'), '918e0ecb43d17e23': ('Application IDs', 'Notepad (32-bit)'), '954ea5f70258b502': ('Application IDs', 'Windows Script Host - wscript.exe (32-bit)'), '9839aec31243a928': ('Application IDs', 'Microsoft Office Excel 2010 x86'), '9b9cdc69c1c24e2b': ('Application IDs', 'Notepad (64-bit)'), '9c7cc110ff56d1bd': ('Application IDs', 'Microsoft Office PowerPoint 2010 x86'), '9f5c7755804b850a': ('Application IDs', 'Windows Script Host - wscript.exe (64-bit)'), 'a18df73203b0340e': ('Application IDs', 'Microsoft Word 2016'), 'a4a5324453625195': ('Application IDs', 'Microsoft Office Word 2013 x86'), 'a7bd71699cd38d1c': ('Application IDs', 'Microsoft Office Word 2010 x86'), 'a8c43ef36da523b1': ('Application IDs', 'Microsoft Office Word 2003 Pinned and Recent.'), 
'adecfb853d77462a': ('Application IDs', 'Microsoft Office Word 2007 Pinned and Recent.'), 'b0459de4674aab56': ('Application IDs', 'Windows Virtual PC - vmwindow.exe (32- and 64-bit)'), 'b74736c2bd8cc8a5': ('Utilities', 'WinZip 15.5 (9468)'), 'b8ab77100df80ab2': ('Application IDs', 'Microsoft Office Excel x64'), 'b8c29862d9f95832': ('Application IDs', 'Microsoft Office InfoPath 2010 x86'), 'b91050d8b077a4e8': ('Application IDs', 'Windows Media Center x64'), 'bc03160ee1a59fc1': ('Application IDs', 'Foxit PDF Reader 5.4.5'), 'be71009ff8bb02a2': ('Application IDs', 'Microsoft Office Outlook x86'), 'c71ef2c372d322d7': ('Application IDs', 'PGP Desktop 10'), 'c765823d986857ba': ('Application IDs', 'Adobe Illustrator CS5 (32-bit)'), 'c7a4093872176c74': ('Application IDs', 'Paint Shop Pro Pinned and Recent.'), 'cdf30b95c55fd785': ('Application IDs', 'Microsoft Office Excel 2007'), 'd00655d2aa12ff6d': ('Application IDs', 'Microsoft Office PowerPoint x64'), 'd38adec6953449ba': ('Application IDs', 'Microsoft Office OneNote 2010 x64'), 'd4a589cab4f573f7': ('Application IDs', 'Microsoft Project 2010 x86'), 'd5c3931caad5f793': ('Application IDs', 'Adobe Soundbooth CS5 (32-bit)'), 'd64d36b238c843a3': ('Application IDs', 'Microsoft Office InfoPath 2010 x86'), 'd7528034b5bd6f28': ('Application IDs', 'Windows Live Mail Pinned and Recent.'), 'e2a593822e01aed3': ('Application IDs', 'Adobe Flash CS5 (32-bit)'), 'e36bfc8972e5ab1d': ('Application IDs', 'XPS Viewer'), 'e70d383b15687e37': ('Application IDs', 'Notepad++ 5.6.8 (32-bit)'), 'f01b4d95cf55d32a': ('Application IDs', 'Windows Explorer Windows 8.1.'), 'f0275e8685d95486': ('Application IDs', 'Microsoft Office Excel 2013 x86'),
'f5ac5390b9115fdb': ('Application IDs', 'Microsoft Office PowerPoint 2007'), 'fb3b0dbfee58fac8': ('Application IDs', 'Microsoft Office Word 365 x86'), '135df2a440abe9bb': ('File Sharing/P2P', 'SoulSeek 156c'), '1434d6d62d64857d': ('File Sharing/P2P', 'BitLord 1.2.0-66'), '223bf0f360c6fea5': ('File Sharing/P2P', 'I2P 0.8.8 (restartable)'), '23f08dab0f6aaf30': ('File Sharing/P2P', 'SoMud 1.3.3'), '2437d4d14b056114': ('File Sharing/P2P', 'EiskaltDC++ 2.2.3'), '2d61cccb4338dfc8': ('File Sharing/P2P', 'BitTorrent 5.0.0 / 6.0.0 / 7.2.1 (Build 25548)'), '2db8e25112ab4453': ('File Sharing/P2P', 'Deluge 1.3.3'), '2ff9dc8fb7e11f39': ('File Sharing/P2P', 'I2P 0.8.8 (no window)'), '3cf13d83b0bd3867': ('File Sharing/P2P', 'RevConnect 0.674p (based on DC++)'), '490c000889535727': ('File Sharing/P2P', 'WinMX 4.9.3.0'), '4a7e4f6a181d3d08': ('File Sharing/P2P', 'broolzShare'), '4aa2a5710da3efe0': ('File Sharing/P2P', 'DCSharpHub 2.0.0'), '4dd48f858b1a6ba7': ('File Sharing/P2P', 'Free Download Manager 3.0 (Build 852)'), '558c5bd9f906860a': ('File Sharing/P2P', 'BearShare Lite 5.2.5.1'), '560d789a6a42ad5a': ('File Sharing/P2P', 'DC++ 0.261 / 0.698 / 0.782 (r2402.1)'), '5b186fc4a0b40504': ('File Sharing/P2P', 'Dtella 1.2.5 (Purdue network only)'), '5d7b4175afdcc260': ('File Sharing/P2P', 'Shareaza 2.0.0.0'), '5e01ecaf82f7d8e': ('File Sharing/P2P', 'Scour Exchange 0.0.0.228'), '5ea2a50c7979fbdc': ('File Sharing/P2P', 'TrustyFiles 3.1.0.22'), '73ce3745a843c0a4': ('File Sharing/P2P', 'FrostWire 5.1.4'), '76f6f1bd18c19698': ('File Sharing/P2P', 'aMule 2.2.6'), '784182360de0c5b6': ('File Sharing/P2P', 'Kazaa Lite 1.7.1'), '792699a1373f1386': ('File Sharing/P2P', 'Piolet 3.1.1'),
'7b7f65aaeca20a8c': ('File Sharing/P2P', 'Dropbox App 5.4.24'), '96252daff039437a': ('File Sharing/P2P', 'Lphant 7.0.0.112351'), '977a5d147aa093f4': ('File Sharing/P2P', 'Lphant 3.51'), '98b0ef1c84088': ('File Sharing/P2P', 'fulDC 6.78'), '99c15cf3e6d52b61': ('File Sharing/P2P', 'mldonkey 3.1.0'), '9ad1ec169bf2da7f': ('File Sharing/P2P', 'FlylinkDC++ r405 (Build 7358)'), 'a31ec95fdd5f350f': ('File Sharing/P2P', 'BitComet 0.49 / 0.59 / 0.69 / 0.79 / 0.89 / 0.99 / 1.07 / 1.28'), 'a746f9625f7695e8': ('File Sharing/P2P', 'HeXHub 5.07'), 'a75b276f6e72cf2a': ('File Sharing/P2P', 'WinMX 3.53'), 'a8df13a46d66f6b5': ('File Sharing/P2P', 'Kommute (Calypso) 0.24'), 'ac3a63b839ac9d3a': ('File Sharing/P2P', 'Vuze 4.6.0.4'), 'accca100973ef8dc': ('File Sharing/P2P', 'Azureus 2.0.8.4'), 'b3016b8da2077262': ('File Sharing/P2P', 'eMule 0.50a'), 'b48ce76eda60b97': ('File Sharing/P2P', 'Shareaza 8.0.0.112300'), 'ba132e702c0147ef': ('File Sharing/P2P', 'KCeasy 0.19-rc1'), 'ba3a45f7fd2583e1': ('File Sharing/P2P', 'Blubster 3.1.1'), 'bcd7ba75303acbcf': ('File Sharing/P2P', 'BitLord 1.1'), 'bfc1d76f16fa778f': ('File Sharing/P2P', 'Ares (Galaxy) 1.8.4 / 1.9.8 / 2.1.0 / 2.1.7.3041'), 'c5ef839d8d1c76f4': ('File Sharing/P2P', 'LimeWire 5.2.13'), 'c8e4c10e5460b00c': ('File Sharing/P2P', 'iMesh 6.5.0.16898'), 'c9374251edb4c1a8': ('File Sharing/P2P', 'BitTornado T-0.3.17'), 'ca1eb46544793057': ('File Sharing/P2P', 'RetroShare 0.5.2a (Build 4550)'), 'caea34d2e74f5c8': ('File Sharing/P2P', 'uTorrent 3.4.7'), 'cb5250eaef7e3213': ('File Sharing/P2P', 'ApexDC++ 1.4.3.957'), 'cbbe886eca4bfc2d': ('File Sharing/P2P', 'ExoSee 1.0.0'), 'cc4b36fbfb69a757': ('File Sharing/P2P', 'gtk-gnutella 0.97'),
'ccb36ff8a8c03b4b': ('File Sharing/P2P', 'Azureus 2.5.0.4 / Vuze 3.0.5.0'), 'cd8cafb0fb6afdab': ('File Sharing/P2P', 'uTorrent 1.7.7 (Build 8179) / 1.8.5 / 2.0 / 2.21 (Build 25113) / 3.0 (Build 25583)'), 'd460280b17628695': ('File Sharing/P2P', 'Java Binary'), 'e0f7a40340179171': ('File Sharing/P2P', 'imule 1.4.5 (rev. 749)'), 'e1d47cb031dafb9f': ('File Sharing/P2P', 'BearShare 6.0.0.22717 / 8.1.0.70928 / 10.0.0.112380'), 'e6ea77a1d4553872': ('File Sharing/P2P', 'Gnucleus 1.8.6.0'), 'e73d9f534ed5618a': ('File Sharing/P2P', 'BitSpirit 1.2.0.228 / 2.0 / 2.6.3.168 / 2.7.2.239 / 2.8.0.072 / 3.1.0.077 / 3.6.0.550'), 'e76a4ef13fbf2bb1': ('File Sharing/P2P', 'Manolito 3.1.1'), 'ecd21b58c2f65a2f': ('File Sharing/P2P', 'StealthNet 0.8.7.9'), 'ed49e1e6ccdba2f5': ('File Sharing/P2P', 'GNUnet 0.8.1a'), 'f001ea668c0aa916': ('File Sharing/P2P', 'Cabos 0.8.2'), 'f1a4c04eebef2906': ('File Sharing/P2P', '[i2p] Robert 0.0.29 Preferences'), 'f214ca2dd40c59c1': ('File Sharing/P2P', 'FrostWire 4.20.9'), 'f61b65550a84027e': ('File Sharing/P2P', 'iMesh 11.0.0.112351'), 'ff224628f0e8103c': ('File Sharing/P2P', 'Morpheus 3.0.3.6'), '10f5a20c21466e85': ('FTP', 'FTP Voyager 15.2.0.17'), '20ef367747c22564': ('FTP', 'Bullet Proof FTP 2010.75.0.75'), '226400522157fe8b': ('FTP', 'FileZilla Server 0.9.39 beta'), '2544ff74641b639d': ('FTP', 'WiseFTP 6.1.5'), '27da120d7e75cf1f': ('FTP', 'pbFTPClient 6.1'), '3198e37206f28dc7': ('FTP', 'CuteFTP 8.3 Professional (Build 8.3.4.0007)'), '3a5148bf2288a434': ('FTP', 'Secure FTP 2.6.1 (Build 20101209.1254)'), '435a2f986b404eb7': ('FTP', 'SmartFTP 4.0.1214.0'), '44a50e6c87bc012': ('FTP', 'Classic FTP Plus 2.15'), '49b5edbd92d8cd58': ('FTP', 'FTP Commander 8.02'),
 '4b632cf2ceceac35': ('FTP', 'Robo-FTP Server 3.2.5'), '4cdf7858c6673f4b': ('FTP', 'Bullet Proof FTP 1.26'), '4fceec8e021ac978': ('FTP', 'CoffeeCup Free FTP 3.5.0.0'), '59e86071b87ac1c3': ('FTP', 'CuteFTP 8.3 (Build 8.3.4.0007)'), '6a316aa67a46820b': ('FTP', 'Core FTP LE 1.3c (Build 1437) / 2.2 (Build 1689)'), '6a8b377d0f5cb666': ('FTP', 'WinSCP 2.3.0 (Build 146)'), '6bb54d82fa42128d': ('FTP', 'WinSCP 4.3.4 (Build 1428)'), '714b179e552596df': ('FTP', 'Bullet Proof FTP 2.4.0 (Build 31)'), '7904145af324576e': ('FTP', 'Total Commander 7.56a (Build 16.12.2010)'), '79370f660ab51725': ('FTP', 'UploadFTP 2.0.1.0'), '7937df3c65790919': ('FTP', 'FTP Explorer 10.5.19 (Build 001)'), '8628e76fd9020e81': ('FTP', 'Fling File Transfer Plus 2.24'), '8deb27dfa31c5c2a': ('FTP', 'CoffeeCup Free FTP 4.4 (Build 1904)'), '8f852307189803b8': ('FTP', 'Far Manager 2.0.1807'), '9560577fd87cf573': ('FTP', 'LeechFTP 1.3 (Build 207)'), '9a3bdae86d5576ee': ('FTP', 'WinSCP 3.2.1 (Build 174) / 3.8.0 (Build 312)'), '9e0b3f677a26bbc4': ('FTP', 'BitKinex 3.2.3'), 'a1d19afe5a80f80': ('FTP', 'FileZilla 2.2.32'), 'a581b8002a6eb671': ('FTP', 'WiseFTP 5.5.9'), 'a79a7ce3c45d781': ('FTP', 'CuteFTP 7.1 (Build 06.06.2005.1)'), 'b6267f3fcb700b60': ('FTP', 'WiseFTP 4.1.0'), 'b7cb1d1c1991accf': ('FTP', 'FlashFXP 4.0.0 (Build 1548)'), 'b8c13a5dd8c455a2': ('FTP', 'Titan FTP Server 8.40 (Build 1338)'), 'be4875bb3e0c158f': ('FTP', 'CrossFTP 1.75a'), 'c04f69101c131440': ('FTP', 'CuteFTP 5.0 (Build 50.6.10.2)'), 'c54b96f328bdc28d': ('FTP', 'WiseFTP 7.3.0'), 'c99ddde925d26df3': ('FTP', 'Robo-FTP 3.7.9 CronMaker'), 'cd2acd4089508507': ('FTP', 'AbsoluteTelnet 9.18 Lite'), 'd28ee773b2cea9b2': ('FTP', '3D-FTP 9.0 build 7'), 
'd8081f151f4bd8a5': ('FTP', 'CuteFTP 8.3 Lite (Build 8.3.4.0007)'), 'e107946bb682ce47': ('FTP', 'FileZilla 3.5.1'), 'e42a8e0f4d9b8dcf': ('FTP', 'Sysax FTP Automation 5.15'), 'e6ef42224b845020': ('FTP', 'ALFTP 5.20.0.4'), 'explorer integrated': ('FTP', 'Swish'), 'f64de962764b9b0f': ('FTP', 'FTPRush 1.1.3 / 2.15'), 'f82607a219af2999': ('FTP', 'Cyberduck 4.1.2 (Build 8999)'), 'f91fd0c57c4fe449': ('FTP', 'ExpanDrive 2.1.0'), 'fa7144034d7d083d': ('FTP', 'Directory Opus 10.0.2.0.4269 (JL tasks supported)'), 'fc999f29bc5c3560': ('FTP', 'Robo-FTP 3.7.9'), '1a60b1067913516a': ('IM/Communications', 'Psi 0.14'), '1b29f0dc90366bb': ('IM/Communications', 'AIM 5.9.3857'), '22cefa022402327d': ('IM/Communications', 'Meca Messenger 5.3.0.52'), '2417caa1f2a881d4': ('IM/Communications', 'ICQ 7.6 (Build 5617)'), '27ececd8d89b6767': ('IM/Communications', 'AIM 6.2.14.2 / 6.5.3.12 / 6.9.17.2'), '2aa756186e21b320': ('IM/Communications', 'RealTimeQuery 3.2'), '2d1658d5dc3cbe2d': ('IM/Communications', 'MySpaceIM 1.0.823.0 Beta'), '30d23723bdd5d908': ('IM/Communications', 'Digsby (Build 30140) (JL support)'), '3461e4d1eb393c9c': ('IM/Communications', 'WTW 0.8.18.2852 / 0.8.19.2940'), '36c36598b08891bf': ('IM/Communications', 'Vovox 2.5.3.4250'), '3c0022d9de573095': ('IM/Communications', 'QuteCom 2.2'), '3f2cd46691bbee90': ('IM/Communications', 'GOIM 1.1.0'), '4278d3dc044fc88a': ('IM/Communications', 'Gaim 1.5.0'), '454ef7dca3bb16b2': ('IM/Communications', 'Exodus 0.10.0.0'), '4e0ac37db19cba15': ('IM/Communications', 'Xfire 1.138 (Build 44507)'), '4f24a7b84a7de5a6': ('IM/Communications', 'Palringo 2.6.3 (r45983)'), '521a29e5d22c13b4': ('IM/Communications', 'Skype 1.4.0.84 / 2.5.0.154 / 3.8.0.139 / 4.2.0.187 / Skype 5.3.0.120 / 5.5.0.115 / 5.5.32.117'),
'6059df4b02360af': ('IM/Communications', 'Kadu 0.10.0 / 0.6.5.5'), '62dba7fb39bb0adc': ('IM/Communications', 'Yahoo Messenger 7.5.0.647 / 8.1.0.421 / 9.0.0.2162 / 10.0.0.1270'), '689319b6547cda85': ('IM/Communications', 'emesene 2.11.7'), '6aa18a60024620ae': ('IM/Communications', 'GCN 2.9.1'), '6f647f9488d7a': ('IM/Communications', 'AIM 7.5.11.9 (custom AppID + JL support)'), '70b52cf73249257': ('IM/Communications', 'Sococo 1.5.0.2274'), '728008617bc3e34b': ('IM/Communications', 'eM Client 3.0.10206.0'), '73c6a317412687c2': ('IM/Communications', 'Google Talk 1.0.0.104'), '74ea779831912e30': ('IM/Communications', 'Skype 7.24.0.104'), '777483d3cdac1727': ('IM/Communications', 'Gajim 0.14.4'), '86b804f7a28a3c17': ('IM/Communications', 'Miranda IM 0.6.8 / 0.7.6 / 0.8.27 / 0.9.9 / 0.9.29 (ANSI + Unicode)'), '884fd37e05659f3a': ('IM/Communications', 'VZOchat 6.3.5'), '8c816c711d66a6b5': ('IM/Communications', 'MSN Messenger 6.2.0137 / 7.0.0820'), '93b18adf1d948fa3': ('IM/Communications', 'qutIM 0.2'), '989d7545c2b2e7b2': ('IM/Communications', 'IMVU 465.8.0.0'), 'a3e0d98f5653b539': ('IM/Communications', 'Instantbird 1.0 (20110623121653) (JL support)'), 'a52b0784bd667468': ('IM/Communications', 'Photos Microsoft 16.526.11220.0 (Windows 10)'), 'a5db18f617e28a51': ('IM/Communications', 'ICQ 6.5 (Build 2024)'), 'aedd2de3901a77f4': ('IM/Communications', 'Pidgin 2.0.0 / 2.10.0 / 2.7.3'), 'b0236d03c0627ac4': ('IM/Communications', 'ICQ 5.1 / ICQLite Build 1068'), 'b06a975b62567622': ('IM/Communications', 'Windows Live Messenger 8.5.1235.0517 BETA'), 'b3965c840bf28ef4': ('IM/Communications', 'AIM 4.8.2616'), 'b868d9201b866d96': ('IM/Communications', 'Microsoft Lync 4.0.7577.0'), 'bcc705f705d8132b': ('IM/Communications', 'Instan-t 5.2 (Build 2824)'), 
'bd249197a6faeff2': ('IM/Communications', 'Windows Live Messenger 2011'), 'bf9ae1f46bd9c491': ('IM/Communications', 'Nimbuzz 2.0.0 (rev 6266)'), 'c312e260e424ae76': ('IM/Communications', 'Mail.RuÂ\xa0Agent 5.8 (JL support)'), 'c5236fd5824c9545': ('IM/Communications', 'PLAYXPERT 1.0.140.2822'), 'c6f7b5bf1b9675e4': ('IM/Communications', 'BitWise IM 1.7.3a'), 'c8aa3eaee3d4343d': ('IM/Communications', 'Trillian 0.74 / 3.1 / 4.2.0.25 / 5.0.0.35 (JL support)'), 'ca942805559495e9': ('IM/Communications', 'aMSN 0.98.4'), 'cca6383a507bac64': ('IM/Communications', 'Gadu-Gadu 10.5.2.13164'), 'd41746b133d17456': ('IM/Communications', 'Tkabber 0.11.1'), 'd7d647c92cd5d1e6': ('IM/Communications', 'uTalk 2.6.4 r47692'), 'da7e8de5b8273a0f': ('IM/Communications', 'Yahoo Messenger 5.0.0.1226 / 6.0.0.1922'), 'dc64de6c91c18300': ('IM/Communications', 'Brosix Communicator 3.1.3 (Build 110719 nid 1)'), 'dee18f19c7e3a2ec': ('IM/Communications', 'PopNote 5.21'), 'e0246018261a9ccc': ('IM/Communications', 'qutIM 0.2.80.0'), 'e0532b20aa26a0c9': ('IM/Communications', 'QQ International 1.1 (2042)'), 'e93dbdcede8623f2': ('IM/Communications', 'Pandion 2.6.106'), 'ebd8c95d87f25154': ('IM/Communications', 'Carrier 2.5.5'), 'efb08d4e11e21ece': ('IM/Communications', 'Paltalk Messenger 10.0 (Build 409)'), 'f09b920bfb781142': ('IM/Communications', 'Camfrog 4.0.47 / 5.5.0 / 6.1 (build 146) (JL support)'), 'f2cb1c38ab948f58': ('IM/Communications', 'X-Chat 1.8.10 / 2.6.9 / 2.8.9'), 'fb1f39d1f230480a': ('IM/Communications', 'Bopup Messenger 5.6.2.9178 (all languages: en;du;fr;ger;rus;es)'), 'fb230a9fe81e71a8': ('IM/Communications', 'Yahoo Messenger 11.0.0.2014-us'), 'fb7ca8059b8f2123': ('IM/Communications', 'ooVoo 3.0.7.21'), '1110d9896dceddb3': ('Image/Document Viewers', 'imgSeek 0.8.5'), 
'169b3be0bc43d592': ('Image/Document Viewers', 'FastPictureViewer Professional 1.6 (Build 211)'), '2519133d6d830f7e': ('Image/Document Viewers', 'IMatch 3.6.0.113'), '2fa14c7753239e4c': ('Image/Document Viewers', 'Paint.NETÂ\xa02.72 / 3.5.8.4081.24580'), '3594aab44bca414b': ('Image/Document Viewers', 'Windows Photo Viewer'), '386a2f6aa7967f36': ('Image/Document Viewers', 'EyeBrowse 2.7'), '3917dd550d7df9a8': ('Image/Document Viewers', 'Konvertor 4.06 (Build 10)'), '3edf100b207e2199': ('Image/Document Viewers', 'digiKam 1.7.0 (KDE 4.4.4)'), '497b42680f564128': ('Image/Document Viewers', 'Zoner PhotoStudio 13 (Build 7)'), '59f56184c796cfd4': ('Image/Document Viewers', 'ACDSee Photo Manager 10 (Build 219)'), '76689ff502a1fd9e': ('Image/Document Viewers', 'Imagine Image and Animation Viewer 1.0.7'), '7cb0735d45243070': ('Image/Document Viewers', 'CDisplay 1.8.1.0'), '8bd5c6433ca967e9': ('Image/Document Viewers', 'ACDSee Photo Manager 2009 (v11.0 Build 113)'), 'b17d3d0c9ca7e29': ('Image/Document Viewers', '"Picasa 3.8.0 (Build 117.43'), 'b39c5f226977725d': ('Image/Document Viewers', 'ACDSee Pro 8.1.99'), 'b3f13480c2785ae': ('Image/Document Viewers', 'Paint 6.1 (build 7601: SP1)'), 'c2d349a0e756411b': ('Image/Document Viewers', 'Adobe Reader 8.1.2'), 'c5c24a503b1727df': ('Image/Document Viewers', 'XnView 1.98.2 Small / 1.98.2 Standard'), 'c634153e7f5fce9c': ('Image/Document Viewers', 'IrfanView 3.10 / 4.30'), 'd33ecf70f0b74a77': ('Image/Document Viewers', '"Picasa 2.2.0 (Build 28.08'), 'd838aac097abece7': ('Image/Document Viewers', 'ACDSee Photo Manager 12 (Build 344)'), 'de48a32edcbe79e4': ('Image/Document Viewers', 'Acrobat Reader 15.x'), 'e31a6a8a7506f733': ('Image/Document Viewers', 'Image AXS Pro 4.1'), 'e9a39dfba105ea23': ('Image/Document Viewers',   'FastStone Image Viewer 4.6'), 
'ea83017cdd24374d': ('Image/Document Viewers', 'IrfanView Thumbnails'), 'edc786643819316c': ('Image/Document Viewers', 'HoneyView3Â\xa0#5834'), 'ee462c3b81abb6f6': ('Image/Document Viewers', 'Adobe Reader X 10.1.0'), 'ef606b196796ebb': ('Image/Document Viewers', 'HP MediaSmart Photo'), 'f0468ce1ae57883d': ('Image/Document Viewers', 'Adobe Reader 7.1.0'), '1461132e553e2e6c': ('Internet Browsers', 'Firefox 6.0'), '16ec093b8f51508f': ('Internet Browsers', 'Opera 8.54 build 7730 / 9.64 build 10487 / 11.50 build 1074'), '1da3c90a72bf5527': ('Internet Browsers', 'Safari 4.0.5 (531.22.7) / 5.1 (7534.50)'), '1eb796d87c32eff9': ('Internet Browsers', 'Firefox 5.0'), '5d696d521de238c3': ('Internet Browsers', 'Chrome 9.0.597.84 / 12.0.742.100 / 13.0.785.215 / 26'), '5df4765359170e26': ('Internet Browsers', 'Firefox 4.0.1'), '8a1c1c7c389a5320': ('Internet Browsers', 'Safari 3.2.3 (525.29)'), '9d1f905ce5044aee': ('Internet Browsers', 'Edge Browser'), 'a0d6b1b874c6e9d2': ('Internet Browsers', 'TOR Browser 6.0.2'), 'cfb56c56fa0f0a54': ('Internet Browsers', 'Mozilla 0.9.9'), '19ccee0274976da8': ('IRC', 'mIRC 4.72 / 5.61'), '2a5a615382a84729': ('IRC', 'X-Chat 2 2.8.6-2'), '54c803dfc87b52ba': ('IRC', 'Nettalk 6.7.12'), '65f7dd884b016ab2': ('IRC', 'LimeChat 2.39'), '6b3a5ce7ad4af9e4': ('IRC', 'IceChat 9 RC2'), '6fee01bd55a634fe': ('IRC', 'Smuxi 0.8.0.0'), '8904a5fd2d98b546': ('IRC', 'IceChat 7.70 20101031'), 'ac8920ed05001800': ('IRC', 'DMDirc 0.6.5 (Profile store: C:\\Users$user\\AppData\\Roaming\\DMDirc)'), 'ae069d21df1c57df': ('IRC', 'mIRC 6.35 / 7.19'), 'b223c3ffbc0a7a42': ('IRC', 'Bersirc 2.2.14'), 'c01d68e40226892b': ('IRC', 'ClicksAndWhistles 2.7.146'), 'd3530c5294441522': ('IRC', 'HydraIRC 0.3.165'), 'dd658a07478b46c2': ('IRC', 'PIRCH98 1.0.1.1190'), 'e30bbea3e1642660': ('IRC', 'Neebly 1.0.4'), 
'fa496fe13dd62edf': ('IRC', 'KVIrc 3.4.2.1 / 4.0.4'), '1cf97c38a5881255': ('Media Players', 'MediaPortal 1.1.3'), '1cffbe973a437c74': ('Media Players', 'DSPlayer 0.889 Lite'), '37392221756de927': ('Media Players', 'RealPlayer SP 12'), '3c93a049a30e25e6': ('Media Players', 'J. River Media Center 16.0.149'), '4a49906d074a3ad3': ('Media Players', 'Media Go 1.8 (Build 121)'), '4acae695c73a28c7': ('Media Players', 'VLC 0.3.0 / 0.4.6'), '4d8bdacf5265a04f': ('Media Players', 'The KMPlayer 2.9.4.1434'), '62bff50b969c2575': ('Media Players', '"Quintessential Media Player 5.0 (Build 121) - also usage stats (times used'), '6bc3383cb68a3e37': ('Media Players', 'iTunes 7.6.0.29 / 8.0.0.35'), '6e9d40a4c63bb562': ('Media Players', 'Real Player Alternative 1.25 (Media Player Classic 6.4.8.2 / 6.4.9.0)'), '7494a606a9eef18e': ('Media Players', 'Crystal Player 1.98'), '7593af37134fd767': ('Media Players', 'RealPlayer 6.0.6.99 / 7 / 8 / 10.5'), '817bb211c92fd254': ('Media Players', 'GOM Player 2.0.12.3375 / 2.1.28.5039'), '90e5e8b21d7e7924': ('Media Players', 'Winamp 3.0d (Build 488)'), '9fda41b86ddcf1db': ('Media Players', 'VLC 0.5.3 / 0.8.6i / 0.9.7 / 1.1.11'), 'a777ad264b54abab': ('Media Players', 'JetVideo 8.0.2.200 Basic'), 'ae3f2acd395b622e': ('Media Players', 'QuickTime Player 6.5.1 / 7.0.3 / 7.5.5 (Build 249.13)'), 'b50ee40805bd280f': ('Media Players', 'QuickTime Alternative 1.9.5 (Media Player Classic 6.4.9.1)'), 'c91d08dcfc39a506': ('Media Players', 'SM Player 0.6.9 r3447'), 'cbeb786f0132005d': ('Media Players', 'VLC 0.7.2'), 'd22ad6d9d20e6857': ('Media Players', 'ALLPlayer 4.7'), 'e40cb5a291ad1a5b': ('Media Players', 'Songbird 1.9.3 (Build 1959)'), 'e6ee34ac9913c0a9': ('Media Players', 'VLC 0.6.2'), 'f674c3a77cfe39d0': ('Media Players', 'Winamp 2.95 / 5.1 / 5.621'), 
'f92e607f9de02413': ('Media Players', 'RealPlayer 14.0.6.666'), 'faef7def55a1d4b': ('Media Players', 'VLC 2.2.6'), 'fe5e840511621941': ('Media Players', 'JetAudio 5.1.9.3018 Basic / 6.2.5.8220 Basic / 7.0.0 Basic / 8.0.16.2000 Basic'), 'eb7e629258d326a1': ('System Cleaners', 'WindowWasher 6.6.1.18'), 'ed7a5cc3cca8d52a': ('System Cleaners', 'CCleaner 1.32.345 / 1.41.544 / 2.36.1233 / 3.10.1525'), '13eb0e5d9a49eaef': ('Usenet Newsreaders', 'Binjet 3.0.2'), '186b5ccada1d986b': ('Usenet Newsreaders', 'NewsGrabber 3.0.36'), '2b164f512891ae37': ('Usenet Newsreaders', 'NewsWolf NSListGen'), '3168cc975b354a01': ('Usenet Newsreaders', 'Slypheed 3.1.2 (Build 1120)'), '36801066f71b73c5': ('Usenet Newsreaders', 'Binbot 2.0'), '36f6bc3efe1d99e0': ('Usenet Newsreaders', 'Alt.Binz 0.25.0 (Build 27.09.2007)'), '3be7b307dfccb58f': ('Usenet Newsreaders', 'NiouzeFire 0.8.7.0'), '3d877ec11607fe4': ('Usenet Newsreaders', 'Thunderbird 6.0.2'), '3ed70ef3495535f7': ('Usenet Newsreaders', 'Gravity 3.0.4'), '3f97341a65bac63a': ('Usenet Newsreaders', 'Ozum 6.07 (Build 6070)'), '43886ba3395acdcc': ('Usenet Newsreaders', 'Easy Post 3.0'), '4d72cfa1d0a67418': ('Usenet Newsreaders', 'Newsgroup Image Collector'), '6224453d9701a612': ('Usenet Newsreaders', 'BinTube 3.7.1.0 (requires VLC 10.5!)'), '7192f2de78fd9e96': ('Usenet Newsreaders', 'TIFNY 5.0.3'), '7526de4a8b5914d9': ('Usenet Newsreaders', 'Forte Agent 6.00 (Build 32.1186)'), '776beb1fcfc6dfa5': ('Usenet Newsreaders', 'Thunderbird 1.0.6 (20050716) / 3.0.2'), '780732558f827a42': ('Usenet Newsreaders', 'AutoPix 5.3.3'), '7a7c60efd66817a2': ('Usenet Newsreaders', 'Spotnet 1.7.4'), '7b2b4f995b54387d': ('Usenet Newsreaders', 'News Reactor 20100224.16'), '7fd04185af357bd5': ('Usenet Newsreaders', 'UltraLeeacher 1.7.0.2969 / 1.8 Beta (Build 3490)'), 
'8172865a9d5185cb': ('Usenet Newsreaders', 'Binreader 1.0 (Beta 1)'), '8211531a7918b389': ('Usenet Newsreaders', 'Newsbin Pro 6.00 (Build 1019) (JL support)'), '86781fe8437db23e': ('Usenet Newsreaders', 'Messenger Pro 2.66.6.3353'), '92f1d5db021cd876': ('Usenet Newsreaders', 'NewsLeecher 4.0 / 5.0 Beta 6'), '9dacebaa9ac8ca4e': ('Usenet Newsreaders', 'TLNews Newsreader 2.2.0 (Build 2430)'), '9f03ae476ad461fa': ('Usenet Newsreaders', 'GroupsAloud 1.0'), 'a4def57ee99d77e9': ('Usenet Newsreaders', 'Nomad News 1.43'), 'aa11f575087b3bdc': ('Usenet Newsreaders', 'Unzbin 2.6.8'), 'ace8715529916d31': ('Usenet Newsreaders', '40tude Dialog 2.0.15.1 (Beta 38)'), 'baea31eacd87186b': ('Usenet Newsreaders', 'BinaryBoy 1.97 (Build 55)'), 'bf483b423ebbd327': ('Usenet Newsreaders', 'Binary Vortex 5.0'), 'bfe841f4d35c92b1': ('Usenet Newsreaders', 'QuadSucker/News 5.0'), 'c02baf50d02056fc': ('Usenet Newsreaders', 'FotoVac 1.0'), 'c845f3a6022d647c': ('Usenet Newsreaders', 'Another File 2.03 (Build 2/7/2004)'), 'c98ab5ccf25dda79': ('Usenet Newsreaders', 'NewsShark 2.0'), 'cb1d97aca3fb7e6b': ('Usenet Newsreaders', 'Newz Crawler 1.9.0 (Build 4100)'), 'cb984e3bc7faf234': ('Usenet Newsreaders', 'NewsRover 17.0 (Rev.0)'), 'cc76755e0f925ce6': ('Usenet Newsreaders', 'AllPicturez 1.2'), 'cd40ead0b1eb15ab': ('Usenet Newsreaders', 'NNTPGrab 0.6.2'), 'cf6379a9a987366e': ('Usenet Newsreaders', 'Digibin 1.31'), 'cfab0ec14b6f953': ('Usenet Newsreaders', 'Express NewsPictures 2.41 (Build 08.05.07.0)'), 'd0261ed6e16b200b': ('Usenet Newsreaders', 'News File Grabber 4.6.0.4'), 'd1fc019238236806': ('Usenet Newsreaders', 'Newsgroup Commander Pro 9.05'), 'd3c5cf21e86b28af': ('Usenet Newsreaders', 'SeaMonkey 2.3.3'), 'd53b52fb65bde78c': ('Usenet Newsreaders', 'Android Newsgroup Downloader 6.2'), 
'd5c02fc7afbb3fd4': ('Usenet Newsreaders', 'NNTPGrab 0.6.2 Server'), 'd7666c416cba240c': ('Usenet Newsreaders', 'NewsMan Pro 3.0.5.2'), 'd7db75db9cdd7c5d': ('Usenet Newsreaders', 'Xnews 5.04.25'), 'dba909a61476ccec': ('Usenet Newsreaders', 'NewsWolf 1.41'), 'de76415e0060ce13': ('Usenet Newsreaders', 'Noworyta News Reader 2.9'), 'eab25958dbddbaa4': ('Usenet Newsreaders', 'Binary News Reaper 2 (Beta 0.14.7.448)'), 'eb3300e672136bc7':('Usenet Newsreaders', 'Stream Reactor 1.0 Beta 9 (uses VLC!)'), 'f920768fe275f7f4': ('Usenet Newsreaders', 'Grabit 1.5.3 Beta (Build 909) / 1.6.2 (Build 940) / 1.7.2 Beta 4 (Build 997)'), '23709f6439b9f03d': ('Utilities', 'Hex Editor Neo 5.14'), '337ed59af273c758': ('Utilities', 'Sticky Notes (Windows 10)'), '3dc02b55e44d6697': ('Utilities', '7-Zip 3.13 / 4.20'), '4975d6798a8bdf66': ('Utilities', '7-Zip 4.65 / 9.20'), '4b6925efc53a3c08': ('Utilities', 'BCWipe 5.02.2 Task Manager 3.02.3'), 'bc0c37e84e063727': ('Utilities', 'Windows Command Processor - cmd.exe (32-bit)'), 'c9950c443027c765': ('Utilities', 'WinZip 9.0 SR-1 (6224) / 10.0 (6667)'), 'e57cfc995bdc1d98': ('Utilities', 'Snagit 11')}
        
        # define the basic information 
        os_root_dir=Path(os.path.expanduser('~'))
        # get the sidstring 
        sidstr = win32security.ConvertSidToStringSid(win32security.GetFileSecurity(".", win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
        # define the lnk files path 
        lnk_path= os_root_dir / 'AppData/Roaming/Microsoft/Windows/Recent/'
         # get the list of lnk files to be parsed
        lnk_files = []
        # check whether the folder is effective
        if os.path.isdir(lnk_path):
            for file in self.dir_walk(lnk_path):
                filename = os.path.basename(file)
                if filename.endswith('.lnk'):
                    lnk_files.append(file)
        else:
            self.print_msg("[-] Error: Path " + str(lnk_path) + " is not directory or not found")
            return None    
        lnk_output = []
        for file in lnk_files:
            self.print_msg("[+] Parse File: " + file)
            if os.path.isfile(file):
                lnk_output += self.automaticDest(file , AppIDs) # parse JumpList
            else:
                self.print_msg("[-] Error: Path " + str(file) + " is not file or not found")
                return None
        # handle all the output results
        self.handle_output_lnk(lnk_output)

        # the following part is use to parser the jumplist
        jumplist_path= os_root_dir / 'AppData/Roaming/Microsoft/Windows/Recent/'
         # get the list of lnk files to be parsed
        jumplist_files = []
        # check whether the folder is effective
        if os.path.isdir(jumplist_path):
            for file in self.dir_walk(jumplist_path):
                filename = os.path.basename(file)
                if filename.endswith('.automaticDestinations-ms') or filename.endswith('.customDestinations-ms'):
                    jumplist_files.append(file)
        else:
            self.print_msg("[-] Error: Path " + str(jumplist_path) + " is not directory or not found")
            return None  

        jumplist_output = []
        for file in jumplist_files:
            self.print_msg("[+] Parse File: " + file)
            if os.path.isfile(file):
                jumplist_output += self.automaticDest(file , AppIDs) # parse JumpList
            else:
                self.print_msg("[-] Error: Path " + str(file) + " is not file or not found")
                return None
        # handle all the output results
        self.handle_output_jumplist(jumplist_output)       

    # if results True then print the msg even if quiet arguments enabled
    # used to print the parsed data
    def print_msg(self, msg , results=False):
        if not self.quiet and results:
            print(msg)


    # return json in a beautifier
    def json_beautifier(self, js):
        return json.dumps(js, sort_keys=True, indent=4)

    def dir_walk(self, path):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                files.append( os.path.join(dirpath , f)  )
        return files

    # this will read the AppID file and return json of all appids 
    def read_AppId(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            appid = {}
            for l in lines:
                fields = l.rstrip().split(',')
                appid[fields[1]] = (fields[0] , fields[2])

            return appid
        return {}

    # File attribute flags
    def get_network_provider_types(self, provider_bytes):
        flags = {
            0x00010000: 'WNNC_NET_MSNET',
            0x00020000: 'WNNC_NET_SMB',
            0x00020000: 'WNNC_NET_LANMAN',
            0x00030000: 'WNNC_NET_NETWARE',
            0x00040000: 'WNNC_NET_VINES',
            0x00050000: 'WNNC_NET_10NET',
            0x00060000: 'WNNC_NET_LOCUS',
            0x00070000: 'WNNC_NET_SUN_PC_NFS',
            0x00080000: 'WNNC_NET_LANSTEP',
            0x00090000: 'WNNC_NET_9TILES',
            0x000A0000: 'WNNC_NET_LANTASTIC',
            0x000B0000: 'WNNC_NET_AS400',
            0x000C0000: 'WNNC_NET_FTP_NFS',
            0x000D0000: 'WNNC_NET_PATHWORKS',
            0x000E0000: 'WNNC_NET_LIFENET',
            0x000F0000: 'WNNC_NET_POWERLAN',
            0x00100000: 'WNNC_NET_BWNFS',
            0x00110000: 'WNNC_NET_COGENT',
            0x00120000: 'WNNC_NET_FARALLON',
            0x00130000: 'WNNC_NET_APPLETALK',
            0x00140000: 'WNNC_NET_INTERGRAPH',
            0x00150000: 'WNNC_NET_SYMFONET',
            0x00160000: 'WNNC_NET_CLEARCASE',
            0x00170000: 'WNNC_NET_FRONTIER',
            0x00180000: 'WNNC_NET_BMC',
            0x00190000: 'WNNC_NET_DCE',
            0x001A0000: 'WNNC_NET_AVID',
            0x001B0000: 'WNNC_NET_DOCUSPACE',
            0x001C0000: 'WNNC_NET_MANGOSOFT',
            0x001D0000: 'WNNC_NET_SERNET',
            0x001E0000: 'WNNC_NET_RIVERFRONT1',
            0x001F0000: 'WNNC_NET_RIVERFRONT2',
            0x00200000: 'WNNC_NET_DECORB',
            0x00210000: 'WNNC_NET_PROTSTOR',
            0x00220000: 'WNNC_NET_FJ_REDIR',
            0x00230000: 'WNNC_NET_DISTINCT',
            0x00240000: 'WNNC_NET_TWINS',
            0x00250000: 'WNNC_NET_RDR2SAMPLE',
            0x00260000: 'WNNC_NET_CSC',
            0x00270000: 'WNNC_NET_3IN1',
            0x00290000: 'WNNC_NET_EXTENDNET',
            0x002A0000: 'WNNC_NET_STAC',
            0x002B0000: 'WNNC_NET_FOXBAT',
            0x002C0000: 'WNNC_NET_YAHOO',
            0x002D0000: 'WNNC_NET_EXIFS',
            0x002E0000: 'WNNC_NET_DAV',
            0x002F0000: 'WNNC_NET_KNOWARE',
            0x00300000: 'WNNC_NET_OBJECT_DIRE',
            0x00310000: 'WNNC_NET_MASFAX',
            0x00320000: 'WNNC_NET_HOB_NFS',
            0x00330000: 'WNNC_NET_SHIVA',
            0x00340000: 'WNNC_NET_IBMAL',
            0x00350000: 'WNNC_NET_LOCK',
            0x00360000: 'WNNC_NET_TERMSRV',
            0x00370000: 'WNNC_NET_SRT',
            0x00380000: 'WNNC_NET_QUINCY',
            0x00390000: 'WNNC_NET_OPENAFS',
            0x003A0000: 'WNNC_NET_AVID1',
            0x003B0000: 'WNNC_NET_DFS',
            0x003C0000: 'WNNC_NET_KWNP',
            0x003D0000: 'WNNC_NET_ZENWORKS',
            0x003E0000: 'WNNC_NET_DRIVEONWEB',
            0x003F0000: 'WNNC_NET_VMWARE',
            0x00400000: 'WNNC_NET_RSFX',
            0x00410000: 'WNNC_NET_MFILES',
            0x00420000: 'WNNC_NET_MS_NFS',
            0x00430000: 'WNNC_NET_GOOGLE',
            0x00440000: 'WNNC_NET_NDFS',
        }

        setFlags = []
        for f in flags.keys():
            if f & provider_bytes == f:
                setFlags.append(flags[f])

        return ','.join(setFlags)

    # Get network share flags 
    def get_network_share_flags(self, network_flag):
        flags = {
            0x0001:    'ValidDevice',
            0x0002:    'ValidNetType'
        }
        setFlags = []
        for f in flags.keys():
            if f & network_flag == f:
                setFlags.append(flags[f])

        return ','.join(setFlags)

    # Get drive type
    def get_drive_type(self, drive_type):
        ids = {
            0:    'DRIVE_UNKNOWN',
            1:    'DRIVE_NO_ROOT_DIR',
            2:    'DRIVE_REMOVABLE',
            3:    'DRIVE_FIXED',
            4:    'DRIVE_REMOTE',
            5:    'DRIVE_CDROM',
            6:    'DRIVE_RAMDISK'
        }
        try:
            return ids[drive_type]
        except Exception as e:
            return 'Unknown'

    # get the Location Flags
    def get_location_flags(self, data_bytes):
        flags = {
            0x0001:    'VolumeIDAndLocalBasePath',
            0x0002:    'CommonNetworkRelativeLinkAndPathSuffix'
        }
        setFlags = []
        for f in flags.keys():
            if f & data_bytes == f:
                setFlags.append(flags[f])

        return ','.join(setFlags)

    # Show Window definitions
    def get_show_window_id(self, data_sw_bytes):
        ids = {
            0:    'SW_HIDE',
            1:    'SW_NORMAL',
            2:    'SW_SHOWMINIMIZED',
            3:    'SW_MAXIMIZE',
            4:    'SW_SHOWNOACTIVATE',
            5:    'SW_SHOW',
            6:    'SW_MINIMIZE',
            7:    'SW_SHOWMINNOACTIVE',
            8:    'SW_SHOWNA',
            9:    'SW_RESTORE',
            10:    'SW_SHOWDEFAULT',
            11:    'SW_FORCEMINIMIZE'
        }
        return ids[data_sw_bytes]

    # File attribute flags
    def get_file_attr_flags(self, data_flag_bytes):
        flags = {
            0x00000001:    'FILE_ATTRIBUTE_READONLY',
            0x00000002:    'FILE_ATTRIBUTE_HIDDEN',
            0x00000004:    'FILE_ATTRIBUTE_SYSTEM',
            0x00000008:    'Unknown',
            0x00000010:    'FILE_ATTRIBUTE_DIRECTORY',
            0x00000020:    'FILE_ATTRIBUTE_ARCHIVE',
            0x00000040:    'FILE_ATTRIBUTE_DEVICE',
            0x00000080:    'FILE_ATTRIBUTE_NORMAL',
            0x00000100:    'FILE_ATTRIBUTE_TEMPORARY',
            0x00000200:    'FILE_ATTRIBUTE_SPARSE_FILE',
            0x00000400:    'FILE_ATTRIBUTE_REPARSE_POINT',
            0x00000800:    'FILE_ATTRIBUTE_COMPRESSED',
            0x00001000:    'FILE_ATTRIBUTE_OFFLINE',
            0x00002000:    'FILE_ATTRIBUTE_NOT_CONTENT_INDEXED',
            0x00004000:    'FILE_ATTRIBUTE_ENCRYPTED',
            0x00008000:    'Unknown',
            0x00010000:    'FILE_ATTRIBUTE_VIRTUAL'
        }

        setFlags = []
        for f in flags.keys():
            if f & data_flag_bytes == f:
                setFlags.append(flags[f])

        return ','.join(setFlags)

    # Data Flags mapping
    def get_data_flags(self, data_flag_bytes):
        flags = {
            0x00000001:    'HasTargetIDList',
            0x00000002:    'HasLinkInfo',
            0x00000004:    'HasName',
            0x00000008:    'HasRelativePath',
            0x00000010:    'HasWorkingDir',
            0x00000020:    'HasArguments',
            0x00000040:    'HasIconLocation',
            0x00000080:    'IsUnicode',
            0x00000100:    'ForceNoLinkInfo',
            0x00000200:    'HasExpString',
            0x00000400:    'RunInSeparateProcess',
            0x00000800:    'Unknown',
            0x00001000:    'HasDarwinID',
            0x00002000:    'RunAsUser',
            0x00004000:    'HasExpIcon',
            0x00008000:    'NoPidlAlias',
            0x00010000:    'Unknown',
            0x00020000:    'RunWithShimLayer',
            0x00040000:    'ForceNoLinkTrack',
            0x00080000:    'EnableTargetMetadata',
            0x00100000:    'DisableLinkPathTracking',
            0x00200000:    'DisableKnownFolderTracking',
            0x00400000:    'DisableKnownFolderAlias',
            0x00800000:    'AllowLinkToLink',
            0x01000000:    'UnaliasOnSave',
            0x02000000:    'PreferEnvironmentPath',
            0x04000000:    'KeepLocalIDListForUNCTarget'
        }
        setFlags = []
        for f in flags.keys():
            if f & data_flag_bytes == f:
                setFlags.append(flags[f])

        return ','.join(setFlags)

    # FILETIME to ISO time format
    def ad_timestamp(self, timestamp , isObject=False):
        timestamp = self.unpack_int_l(timestamp) - (self.unpack_int_l(timestamp) & 0xf000000000000000)

        # if the timestamp extracted from object ID, you need to subtract 5748192000000000 from it
        if isObject:
            timestamp -= 5748192000000000
        #from datetime import datetime,timedelta
        #import datetime
        if timestamp > 0:
            dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp/10)
            return dt.isoformat()
        else:
            return "1700-01-01T00:00:00"

    # unpack the struct of the provided data
    def unpack_int_l(self, data , type='int'):
        if len(data)==1 and type=='int':
            return struct.unpack('<B' , data)[0]
        elif len(data)==2 and type=='int':
            return struct.unpack('<H' , data)[0]
        elif len(data)==4 and type=='int':
            return struct.unpack('<I' , data)[0]
        elif len(data)==4 and type=='singed_int':
            return struct.unpack('<i' , data)[0]
        elif len(data) == 8 and type=='int':
            return struct.unpack('<Q' , data)[0]
        elif len(data)==4 and type=='float':
            return struct.unpack('<f' , data)[0]
        elif len(data)==8 and type=='float':
            return struct.unpack('<d' , data)[0]
        elif len(data)==6 and type=='mac':
            return "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB",data)
        elif type=='uni':
            return data.decode('UTF-16-LE')
        elif type=='printable':
            for codec in self.codecs:
                try:
                    return data.decode(codec,errors='strict')
                except Exception as e:
                    pass
            return self.unpack_int_l(data , 'ascii')

        elif type=='ascii':
            count       = 0
            date_ascii  = ""
            while count < len(data) and chr(data[count]) in string.printable: 
                date_ascii += chr(data[count])
                count +=1 
            return date_ascii
        elif len(data)==16 and type=='uuid':
            return str(uuid.UUID(bytes_le=data))
        else:
            return -1;

    def parse_DestList(self, data):
        
        # ===== parse the DestList Header 
        DestList_header = {
            'Version_Number'            : self.unpack_int_l(data[:4]),
            'Total_Current_Entries'     : self.unpack_int_l(data[4:8]),
            'Total_Pinned_Entries'      : self.unpack_int_l(data[8:12]),
            'Last_Issued_ID_Num'        : self.unpack_int_l(data[16:24]),
            'Number_of_Actions'         : self.unpack_int_l(data[24:32])
        }

        # specify the OS version based on the Version_Number
        Version_Number = {
            1: "Win7/8",
            3: "Win10 build 1511",
            4: 'Win10 build 1607'
        }

        DestList_header['OS_Version'] = Version_Number[DestList_header['Version_Number']] if DestList_header['Version_Number'] in Version_Number.keys() else "Unknown"
        
        # ====== Parse each entry in the DiskList Payload
        DestList_Entries = []
        start_DestList_Entries = 32
        for entry in range(0 , DestList_header['Total_Current_Entries']):
            entry_data = data[start_DestList_Entries:]
            DestList_Entry = {
                'Checksum'                     : hex(self.unpack_int_l(entry_data[0:8])),
                'New_Volume_ID'             : self.unpack_int_l(entry_data[8:24] , 'uuid'),
                'New_Object_ID'             : self.unpack_int_l(entry_data[24:40] , 'uuid'),
                'New_Object_ID_Timestamp'    : self.ad_timestamp(entry_data[24:32] , isObject=True),
                'New_Object_ID_MFT_Seq'        : self.unpack_int_l(entry_data[32:34]),
                'New_Object_ID_MAC_Addr'    : self.unpack_int_l(entry_data[34:40] , 'mac'),
                'Birth_Volume_ID'             : self.unpack_int_l(entry_data[40:56] , 'uuid'),
                'Birth_Object_ID'             : self.unpack_int_l(entry_data[56:72] , 'uuid'),
                'Birth_Object_ID_Timestamp'    : self.ad_timestamp( entry_data[24:32] , isObject=True ),
                'Birth_Object_ID_MFT_Seq'    : self.unpack_int_l(entry_data[64:66]),
                'Birth_Object_ID_MAC_Addr'    : self.unpack_int_l(entry_data[66:72] , 'mac'),
                'NetBIOS'                     : self.unpack_int_l(entry_data[72:88] , 'printable'),
                'Last_Recorded_Access'        : self.ad_timestamp(entry_data[100:108]),
                'Pin_Status_Counter'        : 'unpinned' if self.unpack_int_l(entry_data[108:112]) == 0xFFFFFFFF else str(self.unpack_int_l(entry_data[108:112])),
            }

            # this means it is Windows10 machine not Windows 7/8
            if DestList_header['Version_Number'] == 3 or DestList_header['Version_Number'] == 4: 
                DestList_Entry['Entry_ID_Number'] = self.unpack_int_l(entry_data[88:92])
                DestList_Entry['Access_Counter']  = self.unpack_int_l(entry_data[116:120])

                data_len = self.unpack_int_l(entry_data[128:130])*2

                DestList_Entry['Data'] = self.unpack_int_l(entry_data[130:130+data_len] , 'uni')
                start_DestList_Entries += 130 + data_len + 4

            else:
                DestList_Entry['Entry_ID_Number'] = self.unpack_int_l(entry_data[88:96])
                DestList_Entry['Access_Counter']  = int(self.unpack_int_l(entry_data[96:100] , 'float'))

                data_len = self.unpack_int_l(entry_data[112:114])*2
                DestList_Entry['Data'] = self.unpack_int_l(entry_data[114:114+data_len] , 'uni')
                start_DestList_Entries += 114 + data_len

            DestList_Entries.append(DestList_Entry)

        # merge DestList_Entries and DestList_header
        for e in range(0 , len(DestList_Entries)):
            for d in DestList_header.keys():
                DestList_Entries[e][d] = DestList_header[d]
        return DestList_Entries

    def parse_Lnk(self, stream):
        # ========== Lnk Stream Header
        header_size     = self.unpack_int_l(stream[:4])
        stream_header     = stream[:header_size]
        LnkStreamHeader = {
            'LNK_Class_ID'         : "{" + self.unpack_int_l(stream_header[4:20] , 'uuid') + "}",
            'Data_Flags'        : self.get_data_flags(self.unpack_int_l(stream_header[20:24])),
            'File_Attrbutes'    : self.get_file_attr_flags(self.unpack_int_l(stream_header[24:28])),
            'Time_Creation'        : self.ad_timestamp(stream_header[28:36]),
            'Time_Access'        : self.ad_timestamp(stream_header[36:44]),
            'Time_Modification'    : self.ad_timestamp(stream_header[44:52]),
            'FileSize'            : self.unpack_int_l(stream_header[52:56]),
            'IconIndex'            : self.unpack_int_l(stream_header[56:60] , type='singed_int'),
            'ShowWindow'        : self.get_show_window_id(self.unpack_int_l(stream_header[60:64])),
        }
        
        # ========== Lnk Target ID
        # if the lnk has a target id list
        if "HasTargetIDList" in LnkStreamHeader['Data_Flags']:
            Lnk_Target_ID_Size = self.unpack_int_l(stream[header_size:header_size+2])
            # handle the target id list
            Lnk_Target_ID_Size += 2 # add the first field of link target id (2 bytes defined target id list size)
        else:
            Lnk_Target_ID_Size = 0

        # ========= Location information
        Location_Info_Details = {}
        if "HasLinkInfo" in LnkStreamHeader['Data_Flags']:

            Location_Info_Size             = self.unpack_int_l(stream[header_size+Lnk_Target_ID_Size:header_size+Lnk_Target_ID_Size+4])
            Location_Info_Offset         = header_size+Lnk_Target_ID_Size
            Location_Info_Stream         = stream[Location_Info_Offset:Location_Info_Offset+Location_Info_Size]
            
            Location_Info_Details['Header_Size']         = self.unpack_int_l(Location_Info_Stream[4:8])
            Location_Info_Details['Location_Flags']     = self.get_location_flags(self.unpack_int_l(Location_Info_Stream[8:12]))
            
            # ==== get volume information
            volume_information_offset     = self.unpack_int_l(Location_Info_Stream[12:16]) + Location_Info_Offset
            volume_info_size             = self.unpack_int_l( stream[volume_information_offset:volume_information_offset+4] )
            volume_info                 = stream[volume_information_offset:volume_information_offset+volume_info_size]

            Location_Info_Details['Drive_Type'] = self.get_drive_type(self.unpack_int_l(volume_info[4:8]))
            Location_Info_Details['Drive_SN'] = hex(self.unpack_int_l(volume_info[8:12])).lstrip("0x").upper()

            # get volume label
            if self.unpack_int_l(volume_info[12:16]) <= 16:
                volume_label_offset                 = self.unpack_int_l(volume_info[12:16]) + volume_information_offset 
                volume_label                         = stream[volume_label_offset:volume_label_offset+stream[volume_label_offset:].find(b'\0')]
                
                Location_Info_Details['Volume_Label'] = self.unpack_int_l(volume_label , 'printable')
            else:
                volume_label_offset                 = self.unpack_int_l(volume_info[16:20]) + volume_information_offset
                volume_label                         = stream[volume_label_offset:volume_label_offset+stream[volume_label_offset:].find(b'\0\0')]
                Location_Info_Details['Volume_Label'] = self.unpack_int_l(volume_label , 'uni')

            # ==== local path
            local_path_offset = self.unpack_int_l(Location_Info_Stream[16:20]) + Location_Info_Offset
            Location_Info_Details['Local_Path'] = self.unpack_int_l(stream[local_path_offset:local_path_offset+stream[local_path_offset:].find(b'\0')], 'printable')
            if Location_Info_Details['Header_Size'] > 28:
                local_path_uni_offset = self.unpack_int_l(Location_Info_Stream[28:32]) + Location_Info_Offset

            # ==== network share information
            network_share_offset= self.unpack_int_l(Location_Info_Stream[20:24]) + Location_Info_Offset
            network_share_size     = self.unpack_int_l(stream[network_share_offset:network_share_offset+4])
            network_share_stream= stream[network_share_offset:network_share_offset+network_share_size]

            Location_Info_Details['Network_Share_Flags']     = self.get_network_share_flags(self.unpack_int_l(network_share_stream[4:8]))

            if self.unpack_int_l(network_share_stream[8:12]) > 20:
                Network_Share_Name_offset     = network_share_offset+self.unpack_int_l(network_share_stream[20:24])
            else:
                Network_Share_Name_offset     = network_share_offset+self.unpack_int_l(network_share_stream[8:12])
                Location_Info_Details['Network_Share_Name']     = self.unpack_int_l(stream[Network_Share_Name_offset:Network_Share_Name_offset+stream[Network_Share_Name_offset:].find(b'\0')] , 'printable')
            
            # device name
            if 'ValidDevice' in Location_Info_Details['Network_Share_Flags'] and self.unpack_int_l(network_share_stream[12:16]) != 0:
                Network_Device_Name_offset     = network_share_offset+self.unpack_int_l(network_share_stream[12:16])
                Location_Info_Details['Network_Device_Name'] = self.unpack_int_l(stream[Network_Device_Name_offset:Network_Device_Name_offset+stream[Network_Device_Name_offset:].find(b'\0')] , 'printable')
            
            # network provider type 
            if 'ValidNetType' in Location_Info_Details['Network_Share_Flags'] and self.unpack_int_l(network_share_stream[16:20]) != 0:
                Location_Info_Details['Network_Providers'] = self.get_network_provider_types(self.unpack_int_l(network_share_stream[16:20]))

            # get the information unicode if exists
            if self.unpack_int_l(network_share_stream[8:12]) > 20:
                unicode_network_share_name_offset = self.unpack_int_l(network_share_stream[20:24]) + network_share_offset
                Location_Info_Details['Network_Share_Name_uni'] = self.unpack_int_l(stream[unicode_network_share_name_offset:unicode_network_share_name_offset+stream[unicode_network_share_name_offset:].find(b'\0\0')] , 'uni'),
                if self.unpack_int_l(network_share_stream[24:28]) != 0:
                    unicode_network_decide_name_offset = self.unpack_int_l(network_share_stream[24:28]) + network_share_offset
                    Location_Info_Details['Network_Share_Name_uni'] = self.unpack_int_l(stream[unicode_network_decide_name_offset:unicode_network_decide_name_offset+stream[unicode_network_decide_name_offset:].find(b'\0\0')] , 'uni'),
            # ==== Common Path
            common_path_offset                    = self.unpack_int_l(Location_Info_Stream[24:28]) + Location_Info_Offset
            Location_Info_Details['Common_Path']= self.unpack_int_l(stream[common_path_offset:common_path_offset+stream[common_path_offset:].find(b'\0')] , 'printable')
            # ==== combine all dictionaries
        lnk_details = {}
        for lsh in LnkStreamHeader.keys():
            lnk_details[lsh] = LnkStreamHeader[lsh]
        for lid in Location_Info_Details.keys():
            lnk_details[lid] = Location_Info_Details[lid]
        return lnk_details

    def automaticDest(self, path , AppIDs):
        # check file to get the AppID 
        filename = os.path.basename(path)
        AppID     = "Unknown"
        AppType = "Unknown"
        AppDesc = "Unknown"
        if re.search(r'[0-9A-F]{16}.(AUTOMATICDESTINATIONS-MS|AUTOMATICDESTINATIONS-MS)', filename.upper(), flags = 0):
            AppID = filename.split('.')[0]
            #print(AppID)
            if AppID in AppIDs.keys():
                AppType = AppIDs[AppID][0]
                AppDesc = AppIDs[AppID][1]
        clean_entry = {
                    'LNK_Class_ID'             : '',
                    'Data_Flags'             : '',
                    'File_Attrbutes'         : '',
                    'Time_Creation'         : '',
                    'Time_Access'             : '',
                    'Time_Modification'     : '',
                    'FileSize'                 : '',
                    'IconIndex'             : '',
                    'ShowWindow'             : '',
                    'Header_Size'             : '',
                    'Location_Flags'         : '',
                    'Drive_Type'             : '',
                    'Drive_SN'                 : '',
                    'Volume_Label'             : '',
                    'Local_Path'             : '',
                    'Network_Share_Flags'     : '',
                    'Network_Share_Name'     : '',
                    'Network_Device_Name'     : '',
                    'Network_Providers'     : '',
                    'Network_Share_Name_uni': '',
                    'Common_Path'             : '',
                    'entry_number'             : '',
                    'AppID'                 : AppID,
                    'AppType'                 : AppType,
                    'AppDesc'                 : AppDesc,
                    'Source_Name'             : filename,
                    'Source_Path'             : path
                }

        # if the file is automaticDestinations (Ole Format) then extract the data
        if olefile.isOleFile(path):         
            ole= olefile.OleFileIO(path)
            DestList = {}
            JumpList = []
            for oleDir in ole.listdir():          
                oleDir             = oleDir[0]
                stream             = ole.openstream(oleDir)
                stream_data     = stream.read()
                stream_header     = self.unpack_int_l(stream_data[:4])
                if stream_header != 76:
                    DestList = self.parse_DestList(stream_data[:ole.get_size(oleDir)])
                else:
                    entry_details = self.parse_Lnk(stream_data[:ole.get_size(oleDir)])
                    entry_details['entry_number'] = oleDir
                    JumpList.append( entry_details )      
            for jl in range(0 , len(JumpList)):
                # combine the details of entry from DestList with the details of entry from JumpList 
                for dl in range(0 , len(DestList)):
                    if JumpList[jl]['entry_number'] == DestList[dl]['Entry_ID_Number']:
                        for dl_entry in DestList[dl].keys():
                            JumpList[jl][dl_entry] = DestList[dl][dl_entry]
                # fill empty fields
                for i in clean_entry.keys():
                    if i not in JumpList[jl].keys():
                        JumpList[jl][i] = clean_entry[i]
                JumpList[jl]['Artifact'] = 'JumpList'
            return JumpList
        else:
            # check if the magic header of the file is 4c000000 (LNK) header
            lnk_f = open(path , 'rb')
            lnk_content = lnk_f.read()
            if self.unpack_int_l(lnk_content[:4]) == 76:
                Lnk_Entries = []
                entry_details = self.parse_Lnk(lnk_content)
                # fill empty fields
                for i in clean_entry.keys():
                    if i not in entry_details.keys():
                        entry_details[i] = clean_entry[i]
                entry_details['Artifact'] = 'LNK_File'
                Lnk_Entries.append( entry_details )               
                return Lnk_Entries                      
            else:
                self.print_msg("[-] File " + path + " not a OleFile or LNK file")
            lnk_f.close()
        return []

    # print the output of parsed artifacts
    def handle_output_lnk(self, output):
        def engine():
            engine = create_engine('mysql+pymysql://root:msp21074a.@127.0.0.1/artifacts_v2.9', encoding='utf-8')
            return engine
        output_text = ""
        # json 
        if self.output_format.lower() == 'json':
            output_text = self.json_beautifier( output ) if self.pretty else json.dumps( output )
        # text 
        elif self.output_format.lower() == 'csv':
            output_csv = []
            
            columns = output[0].keys()
            output_csv.append('"' + str('"' + self.delimiter + '"').join(columns) + '"')

            for o in output:
                #print(o)
                temp_output = []
                for c in columns:
                    temp_output.append(str(o[c]))
                output_csv.append('"' + str('"' + self.delimiter + '"').join(temp_output) + '"')
            #print(output_text)
            output_text = '\n'.join(output_csv)
            df_lnk = pd.read_csv(io.StringIO(output_text), lineterminator=',', header=None)
            index_list=[]
            idx=''
            for i in range(len(df_lnk)):
                idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
                index_list.append(idx)
                mac_addr=MAC_addr
            df_lnk.insert(loc=0, column='MAC_addr', value=mac_addr)
            df_lnk.insert(loc=0, column='idx', value=index_list)  
            #print(df)
            df_lnk.to_sql('lnk', con=engine(),if_exists='append',index=False)


    def handle_output_jumplist(self, output):
        def engine():
            engine = create_engine('mysql+pymysql://root:msp21074a.@127.0.0.1/artifacts_v2.9', encoding='utf-8')
            return engine
        output_text = ""
        # json 
        if self.output_format.lower() == 'json':
            output_text = self.json_beautifier( output ) if self.pretty else json.dumps( output ) 
        # text 
        elif self.output_format.lower() == 'csv':
            output_csv = []
            columns = output[0].keys()
            output_csv.append('"' + str('"' + self.delimiter + '"').join(columns) + '"')
            for o in output:
                #print(o)
                temp_output = []
                for c in columns:
                    temp_output.append(str(o[c]))
                output_csv.append('"' + str('"' + self.delimiter + '"').join(temp_output) + '"')
            output_text = '\n'.join(output_csv)
            df_jumplist = pd.read_csv(io.StringIO(output_text), lineterminator=',', header=None)
            # add some extra data
            index_list=[]
            idx=''
            for i in range(len(df_jumplist)):
                idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
                index_list.append(idx)
                mac_addr=MAC_addr
            df_jumplist.insert(loc=0, column='MAC_addr', value=mac_addr)
            df_jumplist.insert(loc=0, column='idx', value=index_list)           
            #print(df)
            df_jumplist.to_sql('jumplist', con=engine(),if_exists='append',index=False)

################################################################################################
# the above is for jumplist and lnk


#This part of the code refers to https://github.com/PoorBillionaire/Windows-Prefetch-Parser
#The  next part is defined for the prefetch  
################################################################################################

class DecompressWin10(object):
    def __init__(self):
        pass

    def tohex(self, val, nbits):
        """Utility to convert (signed) integer to hex."""
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress(self, infile):
        """Utility core."""
        NULL = ctypes.POINTER(ctypes.c_uint)()
        SIZE_T = ctypes.c_uint
        DWORD = ctypes.c_uint32
        USHORT = ctypes.c_uint16
        UCHAR  = ctypes.c_ubyte
        ULONG = ctypes.c_uint32
        # You must have at least Windows 8, or it should fail.
        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
        except AttributeError as e:
            sys.exit("[ - ] {}".format(e) + \
            "\n[ - ] Windows 8+ required for this script to decompress Win10 Prefetch files")
        RtlGetCompressionWorkSpaceSize = \
            ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize
        with open(infile, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()
            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF
            if magic != 0x004d414d :
                sys.exit('Wrong signature... wrong file?')
            if crcck:
                # I could have used RtlComputeCrc32.
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L',0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)          
                if crc != file_crc:
                    sys.exit('{} Wrong file CRC {0:x} - {1:x}!'.format(infile, crc, file_crc))
            compressed_size = len(compressed)
            ntCompressBufferWorkSpaceSize = ULONG()
            ntCompressFragmentWorkSpaceSize = ULONG()
            ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                ctypes.byref(ntCompressBufferWorkSpaceSize),
                ctypes.byref(ntCompressFragmentWorkSpaceSize))
            if ntstatus:
                sys.exit('Cannot get workspace size, err: {}'.format(
                    self.tohex(ntstatus, 32)))
            ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (UCHAR * decompressed_size)()
            ntFinalUncompressedSize = ULONG()
            ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()
            ntstatus = RtlDecompressBufferEx(
                USHORT(calgo),
                ctypes.byref(ntDecompressed),
                ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))
            if ntstatus:
                sys.exit('Decompression failed, err: {}'.format(
                    self.tohex(ntstatus, 32)))

            if ntFinalUncompressedSize.value != decompressed_size:
                sys.exit('Decompressed with a different size than original!')
        return bytearray(ntDecompressed)

########################################
# define the class Prefetch
########################################
class Prefetch(object):
    def __init__(self, infile):
        self.pFileName = infile

        with open(infile, "rb") as f:
            if f.read(3).decode("ASCII") == "MAM":
                f.close()
                d = DecompressWin10()
                decompressed = d.decompress(infile)
                t = tempfile.mkstemp()
                with open(t[1], "wb+") as f:
                    f.write(decompressed)
                    f.seek(0)

                    self.parseHeader(f)
                    self.fileInformation26(f)
                    self.metricsArray23(f)
                    self.traceChainsArray30(f)
                    self.volumeInformation30(f)
                    self.getTimeStamps(self.lastRunTime)
                    self.directoryStrings(f)
                    self.getFilenameStrings(f)
                    return

        with open(infile, "rb") as f:
            self.parseHeader(f)
            
            if self.version == 17:
                self.fileInformation17(f)
                self.metricsArray17(f)
                self.traceChainsArray17(f)
                self.volumeInformation17(f)
                self.getTimeStamps(self.lastRunTime)
                self.directoryStrings(f)
            
            elif self.version == 23:
                self.fileInformation23(f)
                self.metricsArray23(f)
                self.traceChainsArray17(f)
                self.volumeInformation23(f)
                self.getTimeStamps(self.lastRunTime)
                self.directoryStrings(f)

            elif self.version == 26:
                self.fileInformation26(f)
                self.metricsArray23(f)
                self.traceChainsArray17(f)
                self.volumeInformation23(f)
                self.getTimeStamps(self.lastRunTime)
                self.directoryStrings(f)

            self.getFilenameStrings(f)

    def parseHeader(self, infile):
        # Parse the file header
        # 84 bytes
        self.version = struct.unpack_from("I", infile.read(4))[0]
        self.signature = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = struct.unpack_from("I", infile.read(4))[0]
        self.fileSize = struct.unpack_from("I", infile.read(4))[0]
        self.executableName = struct.unpack_from("60s", infile.read(60))[0].decode("UTF-16", errors="backslashreplace").split("\x00")[0]
        rawhash = hex(struct.unpack_from("I", infile.read(4))[0])
        self.hash = rawhash.lstrip("0x")
        unknown1 = infile.read(4)

    def fileInformation17(self, infile):
        # File Information
        # 68 bytes
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        self.lastRunTime = infile.read(8)
        unknown0 = infile.read(16)
        self.runCount = struct.unpack_from("I", infile.read(4))[0]
        unknown1 = infile.read(4)

    def metricsArray17(self, infile):
        # File Metrics Array
        # 20 bytes
        unknown0 = infile.read(4)
        unknown1 = infile.read(4)
        self.filenameOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameLength = struct.unpack_from("I", infile.read(4))[0]
        unknown2 = infile.read(4)

    def traceChainsArray17(self, infile):
        # Read through the Trace Chains Array
        # Not being parsed for information
        # Broken out as its own function for possible future use
        # 12 bytes
        infile.read(12)

    def volumeInformation17(self, infile):
        # Volume information
        # 40 bytes per entry in the array
        
        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []

        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0]
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            self.volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = self.volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefSize = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(4)

            self.directoryStringsArray.append(self.directoryStrings(infile))

            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2)
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)
            
            count += 1
            infile.seek(self.volumesInformationOffset + (40 * count))

    def fileInformation23(self, infile):
        # File Information
        # 156 bytes
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = infile.read(8)
        self.lastRunTime = infile.read(8)
        unknown1 = infile.read(16)
        self.runCount = struct.unpack_from("I", infile.read(4))[0]
        unknown2 = infile.read(84)

    def metricsArray23(self, infile):
        # File Metrics Array
        # 32 bytes per array, not parsed in this script
        infile.seek(self.metricsOffset)
        unknown0 = infile.read(4)
        unknown1 = infile.read(4)
        unknown2 = infile.read(4)
        self.filenameOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameLength = struct.unpack_from("I", infile.read(4))[0]
        unknown3 = infile.read(4)
        self.mftSeqNumber, self.mftEntryNumber = self.convertFileReference(infile.read(8))
        #self.mftSeqNumber = struct.unpack_from("H", infile.read(2))[0]

    def volumeInformation23(self, infile):
        # This function consumes the Volume Information array
        # 104 bytes per structure in the array
        # Returns a dictionary object which holds another dictionary
        # for each volume information array entry

        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []
        
        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0]
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(68)

            self.directoryStringsArray.append(self.directoryStrings(infile))
            
            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2)
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)
            
            count += 1
            infile.seek(self.volumesInformationOffset + (104 * count))

    def fileInformation26(self, infile):
        # File Information
        # 224 bytes
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = infile.read(8)
        self.lastRunTime = infile.read(64)
        unknown1 = infile.read(16)
        self.runCount = struct.unpack_from("I", infile.read(4))[0]
        unknown2 = infile.read(96)

    def traceChainsArray30(self, infile):
        # Trace Chains Array
        # Read though, not being parsed for information
        # Broken out as its own function for possible future use
        # 8 bytes
        infile.read(8)

    def volumeInformation30(self, infile):
        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []
        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0] 
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            self.volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = self.volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(60)

            self.directoryStringsArray.append(self.directoryStrings(infile))

            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2)
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)
            
            count += 1
            infile.seek(self.volumesInformationOffset + (96 * count))

    def getFilenameStrings(self, infile):
        # Parses filename strings from the PF file
        infile.seek(self.filenameStringsOffset)
        self.filenames = infile.read(self.filenameStringsSize)
        self.resources = self.filenames.decode("UTF-16", errors="backslashreplace").split("\x00")[:-1]


    def convertTimestamp(self, timestamp):
        from datetime import datetime,timedelta
        # Timestamp is a Win32 FILETIME value
        # This function returns that value in a human-readable format
        return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))


    def getTimeStamps(self, lastRunTime):
        self.timestamps = []

        for timestamp in range(8):
            try:
                start_ts = timestamp * 8
                ts = struct.unpack_from("Q", lastRunTime[start_ts:start_ts + 8])[0]
                if ts:
                    self.timestamps.append(convertTimestamp(ts))
            except struct.error:
                return self.timestamps


    def directoryStrings(self, infile):
        infile.seek(self.volumesInformationOffset)
        infile.seek(self.dirStringsOffset, 1)

        directoryStrings = []

        count = 0
        while count < self.dirStringsCount:
            # Below we account for the NULL byte, which is not included in stringLength
            stringLength = struct.unpack_from("<H", infile.read(2))[0] * 2 + 2
            directoryStrings.append((infile.read(stringLength).decode("UTF-16", errors="backslashreplace")))
            count += 1
        return directoryStrings


    def convertFileReference(self, buf):
        sequenceNumber = int.from_bytes(buf[-2:], byteorder="little")
        entryNumber = int.from_bytes(buf[0:6], byteorder="little")
        return sequenceNumber, entryNumber


    def prettyPrint(self):
        pf_result=[]
        # Prints important Prefetch data in a structured format
        banner = "=" * (len(ntpath.basename(self.pFileName)) + 2)
        #print("\n{0}\n{1}\n{0}\n".format(banner, ntpath.basename(self.pFileName)))
        #print("Executable Name: {}\n".format(self.executableName))
        #print("Run count: {}\n".format(self.runCount))
        pf_result.append(self.pFileName)
        pf_result.append(self.executableName)
        pf_result.append(self.runCount)    

        '''
        if len(self.timestamps) > 1:
            #print("Last Executed:")
            for timestamp in self.timestamps:
                print("    " + timestamp)
        else:
            print("Last Executed: {}".format(self.timestamps[0]))
        ''' 
        # run time infor
        run_t=''
        for run_time in self.timestamps:
            run_t += '\n' + str(run_time) +'\n'
        pf_result.append(run_t)
        
        #print("\nVolume Information:")
        for i in self.volumesInformationArray:
            #print(i)
            #print("   Volume Name: " + i["Volume Name"].decode("UTF-16", errors="backslashreplace"))
            #print("   Creation Date: " + i["Creation Date"])
            #print("   Serial Number: " + i["Serial Number"])
            #print()
            pass
        
        if (len(self.volumesInformationArray)<2):
            pf_result.append((self.volumesInformationArray[0])['Volume Name'].decode("UTF-16", errors="backslashreplace"))
            pf_result.append((self.volumesInformationArray[0])['Creation Date'])
            pf_result.append((self.volumesInformationArray[0])['Serial Number'])
            pf_result.append(' ')
            pf_result.append(' ')
            pf_result.append(' ')

        else:
            pf_result.append((self.volumesInformationArray[0])['Volume Name'].decode("UTF-16", errors="backslashreplace"))
            pf_result.append((self.volumesInformationArray[0])['Creation Date'])
            pf_result.append((self.volumesInformationArray[0])['Serial Number'])
            pf_result.append((self.volumesInformationArray[1])['Volume Name'].decode("UTF-16", errors="backslashreplace"))
            pf_result.append((self.volumesInformationArray[1])['Creation Date'])
            pf_result.append((self.volumesInformationArray[1])['Serial Number'])
             
        #print(pf_result)        
        
        dir=''
        for volume in self.directoryStringsArray:
            for dirstring in enumerate(volume):
                #print("{:>4}: {}".format(dirstring[0], dirstring[1]))
                dir+= '\n' + str(dirstring[0])+' '+str(dirstring[1]) + '\n'
                #pass
        pf_result.append(dir)
        res=''
        for resource in enumerate(self.resources):
            #print("{:>4}: {}".format(resource[0], resource[1]))
            res+= '\n'+ str(resource[0])+' '+str(resource[1])
        pf_result.append(res)
        #print(res)
        return pf_result 


def convertTimestamp(timestamp):
        from datetime import datetime,timedelta
        # Timestamp is a Win32 FILETIME value
        # This function returns that value in a human-readable format
        return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))

# define the parsed_Prefetch() 
##########################################################################################33

def parsed_Prefetch():    
   
    #pf_path='C:\\Users\\Zhu_Y\\Desktop\\Projects\\windowsprefetch\\scripts\\pre'
    pf_path='C:\\Windows\\Prefetch'
    file_paths = []
    # folder or a single file both ok 
    if os.path.isdir(pf_path):
        for filename in os.listdir(pf_path):
            file_paths.append(os.path.join(pf_path, filename))
    else:
        file_paths.append(pf_path)

    # create a list to store the unparsed file
    unparsed_files = []
    for filepath in file_paths:
        if filepath.endswith(".pf"):
            if os.path.getsize(filepath) > 0:
                unparsed_file = Prefetch(filepath)
                unparsed_files.append(unparsed_file)

    # parse those unparsed files 
    i=1
    for parsed_pf in unparsed_files:
        #print(parsed_pf)
        idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
        PF_result=parsed_pf.prettyPrint()
        #print(PF_result[3])
        sql="""insert into prefetch (idx, MAC_addr, Pf_name, EXE_name, Run_count, last_run, Vol_0_name, Vol_0_create_T, Vol_0_SN, Vol_1_name, Vol_1_create_T, Vol_1_SN, Directory_Strings, Resources) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        curs.execute(sql,(idx,MAC_addr,PF_result[0],PF_result[1],PF_result[2],PF_result[3],PF_result[4],PF_result[5],PF_result[6],PF_result[7],PF_result[8],PF_result[9],PF_result[10],PF_result[11]))
        conn.commit()
        i+=1

################################################################################################3
# the above is defined for the prefetch


################################################################################################
# the next part is defined for the recycle_bin

import win32security
from pathlib import Path

class deleted_file():
    def __init__(self):
        self.date = None
        self.size = None
        self.type = ''
        self.Ifile = ''
        self.Rfile = ''
        self.filepath = ''
        self.filename = ''
        self.file_dir = ''

def to_seconds(date):
    # https://stackoverflow.com/questions/6256703/convert-64bit-timestamp-to-a-readable-value
    s = float(date) / 1e7  # convert to seconds
    seconds = s - 11644473600  # number of seconds from 1601 to 1970
    # 'Sat Jan 26 03:27:21 2019'
    import datetime
    #from datetime import datetime,timedelta
    return datetime.datetime.strptime(time.ctime(seconds), '%a %b %d %H:%M:%S %Y')

def parsed_Recyclebin():
    full_display = 1
    deleted_files = []
    sidstr = win32security.ConvertSidToStringSid(win32security.GetFileSecurity(".", win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
    RecycleBin1=str(Path('C:\\$Recycle.Bin') / sidstr)
    RecycleBin2=str(Path('D:\\$Recycle.Bin') / sidstr)
    RecycleBin3=str(Path('E:\\$Recycle.Bin') / sidstr) 
    RecycleBin4=str(Path('F:\\$Recycle.Bin') / sidstr)
    RecycleBin5=str(Path('F:\\$Recycle.Bin') / sidstr)
    RB=[]
    RB.append(RecycleBin1)
    RB.append(RecycleBin2)
    RB.append(RecycleBin3)
    RB.append(RecycleBin4)
    RB.append(RecycleBin5)
    
    for RecycleBin in RB:
        if(os.path.exists(RecycleBin)):
        # del_file = None
            if os.path.isdir(RecycleBin.strip()):
                for root, dirs, files in os.walk(RecycleBin):
                    for file in files:
                        if file[0:2] == '$I':
                            with open(os.path.join(root, file), "rb") as f:
                                del_file = deleted_file()
                                del_file.Ifile = os.path.join(root, file)
                                del_file.Rfile = os.path.join(root, file.replace('$I', '$R'))
                                header = f.read(8)
                                size = f.read(8)
                                del_file.size = int.from_bytes(size, byteorder='little')
                                date = f.read(8)
                                if header == b'\x02\x00\x00\x00\x00\x00\x00\x00':
                                    filename_length = f.read(4)
                                del_file.filepath = str(f.read(), 'latin-1').replace('\x00', '').encode('ascii', 'ignore').decode('utf-8')
                                del_file.date = to_seconds(struct.unpack("<Q", date)[0])
                                del_file.filename = del_file.filepath.split('\\')[-1:][0]
                                if os.path.isdir(del_file.Rfile):
                                    del_file.type = "dir"
                                elif os.path.isfile(del_file.Rfile):
                                    del_file.type = "file"
                                deleted_files.append(del_file)
            elif os.path.isfile(RecycleBin.strip()):
                if os.path.basename(RecycleBin)[0:2] == '$I':
                    with open(RecycleBin, "rb") as f:
                        del_file = deleted_file()
                        del_file.Ifile = RecycleBin.strip()
                        del_file.Rfile = RecycleBin.replace('$I', '$R').strip()
                        header = f.read(8)
                        size = f.read(8)
                        del_file.size = int.from_bytes(size, byteorder='little')
                        date = f.read(8)
                        if header == b'\x02\x00\x00\x00\x00\x00\x00\x00':
                            filename_length = f.read(4)
                        del_file.filepath = str(f.read(), 'latin-1').replace('\x00', '').encode('ascii', 'ignore').decode('utf-8')
                        del_file.date = to_seconds(struct.unpack("<Q", date)[0])
                        del_file.filename = del_file.filepath.split('\\')[-1:][0]
                        if os.path.isdir(del_file.Rfile):
                            del_file.type = "dir"
                        elif os.path.isfile(del_file.Rfile):
                            del_file.type = "file"
                            print(del_file.Ifile)
                        deleted_files.append(del_file)
                        
            # create table for the $recycle_bin 
            i=1
            for del_file in deleted_files:
                idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
                if del_file.type == "dir":
                    sql="""insert into recycle_bin(idx,MAC_addr,deleted_date,file_type,file_size,file_path,file_name,ifile_name,rfile_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    curs.execute(sql,(idx,MAC_addr, del_file.date, del_file.type, del_file.size, del_file.filepath.strip(), del_file.filename.strip(), os.path.basename(del_file.Ifile),os.path.basename(del_file.Rfile)))
                    conn.commit()
                    if full_display: # if full_display, then the function will 
                        for root, dir, files in os.walk(del_file.Rfile):
                            for file in files:
                                sql="""insert into recycle_bin(idx, MAC_addr, deleted_date,file_type,file_size,file_path,file_name) values (%s,%s,%s,%s,%s,%s,%s)"""
                                curs.execute(sql,(idx, MAC_addr, del_file.date, "dir content", os.path.getsize(os.path.join(root, file)),os.path.join(del_file.filepath, file).replace("/", "\\"), file))
                                conn.commit()
                #elif del_file.type == "file":
                else:
                    #pass
                    sql="""insert into recycle_bin(idx, MAC_addr, deleted_date,file_type,file_size,file_path,file_name,ifile_name,rfile_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    curs.execute(sql,(idx,MAC_addr, del_file.date, del_file.type, del_file.size, del_file.filepath.strip(), del_file.filename.strip(),os.path.basename(del_file.Ifile),os.path.basename(del_file.Rfile)))
                    conn.commit()
                
                i+=1
                        
            # create table for the $recycle_bin 
            i=1
            for del_file in deleted_files:
                idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
                if del_file.type == "dir":
                    sql="""insert into recycle_bin(idx,MAC_addr,deleted_date,file_type,file_size,file_path,file_name,ifile_name,rfile_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    curs.execute(sql,(idx,MAC_addr, del_file.date, del_file.type, del_file.size, del_file.filepath.strip(), del_file.filename.strip(), os.path.basename(del_file.Ifile),os.path.basename(del_file.Rfile)))
                    conn.commit()
                    if full_display: # if full_display, then the function will 
                        for root, dir, files in os.walk(del_file.Rfile):
                            for file in files:
                                sql="""insert into recycle_bin(idx, MAC_addr, deleted_date,file_type,file_size,file_path,file_name) values (%s,%s,%s,%s,%s,%s,%s)"""
                                curs.execute(sql,(idx, MAC_addr, del_file.date, "dir content", os.path.getsize(os.path.join(root, file)),os.path.join(del_file.filepath, file).replace("/", "\\"), file))
                                conn.commit()
                #elif del_file.type == "file":
                else:
                    #pass
                    sql="""insert into recycle_bin(idx, MAC_addr, deleted_date,file_type,file_size,file_path,file_name,ifile_name,rfile_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    curs.execute(sql,(idx,MAC_addr, del_file.date, del_file.type, del_file.size, del_file.filepath.strip(), del_file.filename.strip(),os.path.basename(del_file.Ifile),os.path.basename(del_file.Rfile)))
                    conn.commit()
                
                i+=1

##################################################################################################
# the above is used to support the recycle_bin



##################################################################################################
# the next part i support the windows 10 timeline

def get_activity(cursor):
    #print('[+] Extracting data from Activity Table')
    cursor.execute('''
        SELECT
            datetime(Activity.LastModifiedTime,'unixepoch') AS 'Last Modified Time',
            datetime(Activity.ExpirationTime, 'unixepoch') AS 'Expiration Time',
            datetime(Activity.LastModifiedOnClient, 'unixepoch') AS 'Last Modification Time on Client',
            datetime(Activity.StartTime, 'unixepoch') AS 'Start Time',
            CASE
                WHEN Activity.CreatedInCloud == 0
                THEN ''
                ELSE datetime(Activity.CreatedInCloud, 'unixepoch')
            END AS 'Created In Cloud',
            Activity.ETag AS 'ETag',
            CASE
                WHEN ActivityType in (2, 11, 12, 15, 16) THEN json_extract(Activity.AppId, '$[0].application')
                WHEN json_extract(Activity.AppId, '$[0].platform') == 'afs_crossplatform' THEN json_extract(Activity.AppId, '$[1].application') ELSE json_extract(Activity.AppId, '$[0].application')
            END AS 'Application',
            CASE
                WHEN
                    Activity.ActivityType == 5
                THEN
                    json_extract(Activity.Payload, '$.appDisplayName')
            END AS 'Display Name',
            CASE
                WHEN
                    Activity.ActivityType == 5
                THEN
                    json_extract(Activity.Payload, '$.displayText')
            END AS 'Display Text',
            CASE
                WHEN ActivityType == 5 THEN 'User Opened app/file/page (5)'
                WHEN ActivityType == 6 THEN 'App in use/focus (6)'
                WHEN ActivityType in (11, 12, 15) THEN 'System ('||ActivityType||')'
                WHEN ActivityType == 16 THEN 'Copy/Paste (16)'
                ELSE ActivityType
            END AS "Activity Type",
            CASE
                WHEN ActivityStatus == 1 THEN 'Active'
                WHEN ActivityStatus == 2 THEN 'Updated'
                WHEN ActivityStatus == 3 THEN 'Deleted'
                WHEN ActivityStatus == 4 THEN 'Ignored'
            END AS 'Activity Status',
            Activity.Priority,
            CASE
                WHEN Activity.IsLocalOnly == 0
                THEN 'No'
                ELSE 'Yes'
            END AS 'Is Local Only',
            CASE
                WHEN Activity.Tag NOT NULL
                THEN Activity.Tag
                ELSE ''
            END AS 'Tag',
            CASE
                WHEN Activity."Group" NOT NULL
                THEN Activity."Group"
                ELSE ''
            END AS 'Group',
            CASE
                WHEN Activity.MatchId NOT NULL
                THEN Activity.MatchId
                ELSE ''
            END AS 'Match ID',
            CASE
                WHEN json_extract(Activity.AppId,'$[0].platform') == 'afs_crossplatform'
                THEN json_extract(Activity.AppId,'$[1].platform')
                ELSE json_extract(Activity.AppId,'$[0].platform')
            END AS 'Platform',
            CASE 
		        WHEN Activity.ActivityType==5 THEN json_extract(Activity.Payload, '$.description') 
		        ELSE '' 
	        END AS 'Description',
        	CASE
    		    WHEN Activity.ActivityType==5 THEN json_extract(Activity.Payload, '$.contentUri') 
    		    ELSE '' 
	        END AS 'Content Uri',
            Activity.AppActivityId,
            CASE
                WHEN hex(Activity.ParentActivityId) == '00000000000000000000000000000000'
                THEN ''
                ELSE hex(Activity.ParentActivityId)
            END AS 'Parent Activity Id',
            Activity.PlatformDeviceId AS 'Platform Device Id',
            Activity.DdsDeviceId AS 'Dds Device Id',
            CASE
                WHEN Activity.ActivityType == 16 THEN json_extract(Activity.Payload, '$.clipboardDataId')
                ELSE ''
            END AS 'Clipboard Data ID',
            CASE
                WHEN Activity.ActivityType == 10 THEN json_extract(Activity.ClipboardPayload, '$[0].content')
                ELSE ''
            END AS 'Clipboard Data',
            CASE
                WHEN Activity.ActivityType == 16 THEN json_extract(Activity.Payload, '$.gdprType')
                ELSE ''
            END AS 'GDPR Type',
            Activity.PackageIdHash,
            Activity.Payload AS 'Original Payload'
        FROM
            Activity
        ORDER BY 
            Activity.ETag;
    ''')

    all_rows = cursor.fetchall()

    return all_rows

def get_activityOperation(cursor):
    print('[+] Extracting data from ActivityOperation Table')

    cursor.execute('''
        SELECT
	        datetime(ActivityOperation.CreatedTime, 'unixepoch') AS 'Created Time',
	        datetime(ActivityOperation.LastModifiedTime,'unixepoch') AS 'Last Modified Time',
	        datetime(ActivityOperation.LastModifiedOnClient, 'unixepoch') AS 'Last Modification Time on Client',
	        datetime(ActivityOperation.ExpirationTime, 'unixepoch') AS 'Expiration Time',
	        datetime(ActivityOperation.OperationExpirationTime, 'unixepoch') AS 'Operation Expiration Time',
	        datetime(ActivityOperation.StartTime, 'unixepoch') AS 'Start Time',
	        CASE
	        	WHEN ActivityOperation.EndTime == 0
	        	THEN ''
	        	ELSE datetime(ActivityOperation.EndTime, 'unixepoch')
	        END AS 'End Time',
	        CASE
	        	WHEN ActivityOperation.CreatedInCloud == 0 THEN ''
	        	ELSE datetime(ActivityOperation.CreatedInCloud, 'unixepoch')
	        END AS 'Created In Cloud',
	        ActivityOperation.ETag AS 'ETag',
	        CASE
	        	WHEN ActivityType in (2, 11, 12, 15, 16) THEN json_extract(ActivityOperation.AppId, '$[0].application')
	        	WHEN json_extract(ActivityOperation.AppId, '$[0].platform') == 'afs_crossplatform' THEN json_extract(ActivityOperation.AppId, '$[1].application') ELSE json_extract(ActivityOperation.AppId, '$[0].application')
	        END AS 'Application',
	        CASE
	        	WHEN ActivityType == 5
	        	THEN json_extract(ActivityOperation.Payload, '$.displayText')
	        END AS 'Display Text',
	        CASE
	        	WHEN ActivityType == 5 
	        	THEN json_extract(ActivityOperation.Payload, '$.appDisplayName')
	        END AS 'App Display Name',
	        CASE
	        	WHEN ActivityType == 5 THEN 'User Opened app/file/page (5)'
                WHEN ActivityType == 6 THEN 'App in use/focus (6)'
                WHEN ActivityType in (11, 12, 15) THEN 'System ('||ActivityType||')'
                WHEN ActivityType == 16 THEN 'Copy/Paste (16)'
                ELSE ActivityType
	        END AS "Activity Type",
	        CASE
	        	WHEN ActivityOperation.ActivityType == 6
	        	THEN time(json_extract(ActivityOperation.Payload,'$.activeDurationSeconds'),'unixepoch')
	        	ELSE ''
	        END AS 'Active Duration',
	        CASE
	        	WHEN ActivityOperation.ActivityType == 6 and ((ActivityOperation.EndTime - ActivityOperation.StartTime) > 0)
	        	THEN time((ActivityOperation.EndTime - ActivityOperation.StartTime), 'unixepoch')
	        	ELSE ''
	        END AS 'Calculated Active Duration',
	        ActivityOperation.Priority,
	        CASE
	        	WHEN ActivityOperation.OperationType == 1 THEN 'Active'
	        	WHEN ActivityOperation.OperationType == 2 THEN 'Updated'
	        	WHEN ActivityOperation.OperationType == 3 THEN 'Deleted'
	        	WHEN ActivityOperation.OperationType == 4 THEN 'Ignored'
	        END AS 'Operation Type',
	        CASE
	        	WHEN ActivityOperation.ActivityType == 6
	        	THEN json_extract(ActivityOperation.Payload,'$.userTimezone')
	        	ELSE ''
	        END AS 'User Engaged Timezone',
	        CASE 
	        	WHEN ActivityOperation.ActivityType==5 THEN json_extract(ActivityOperation.Payload, '$.description') 
	        	ELSE '' 
	        END AS 'Description',
	        CASE
	        	WHEN ActivityOperation.ActivityType==5 THEN json_extract(ActivityOperation.Payload, '$.contentUri') 
	        	ELSE '' 
	        END AS 'Content Uri',
	        hex(ActivityOperation.Id) AS 'ID',
	        ActivityOperation.Tag AS 'Tag',
	        ActivityOperation.MatchId AS 'Match ID',
	        CASE
	        	WHEN ActivityOperation.ActivityType in (2,11,12,15) 
	        	then ''
	        	else coalesce(json_extract(ActivityOperation.Payload, '$.activationUri'),json_extract(ActivityOperation.Payload, '$.reportingApp')) 
	        end as 'App/Uri',
	        ActivityOperation."Group",
	        ActivityOperation.AppActivityId,
	        CASE 
	        	WHEN hex(ActivityOperation.ParentActivityId) == '00000000000000000000000000000000'
	        	THEN ''
	        	ELSE hex(ActivityOperation.ParentActivityId)
            END AS 'Parent Activity Id',
	        ActivityOperation.PlatformDeviceId AS 'Platform Device Id',
	        ActivityOperation.DdsDeviceId AS 'Dds Device Id',
	        ActivityOperation.GroupAppActivityId AS 'Group App Activity Id',
	        ActivityOperation.EnterpriseId AS 'EnterpriseId',
	        ActivityOperation.PackageIdHash AS 'Package Id Hash',
	        ActivityOperation.Payload AS 'Orignal Payload'
	    FROM
	        ActivityOperation
	    ORDER BY ActivityOperation.ETag;
    ''')

    all_rows = cursor.fetchall()
    return all_rows

def get_packageID(cursor):
    #print('[+] Extracting data from Activity_PackageID Table')
    cursor.execute('''
        SELECT
	        hex(ActivityId), 
        	Platform, 
	        PackageName, 
        	datetime(ExpirationTime, 'unixepoch') 
	    FROM 
	        Activity_PackageId;
    ''')
    all_rows = cursor.fetchall()
    return all_rows

def activitycacheparser():

       #ActivitiesCache_db_path = 'C:\\Users\\Zhu_Y\\AppData\\Local\\ConnectedDevicesPlatform\\L.Zhu_Y\\ActivitiesCache.db'
    input_db=str(Path(os.path.expanduser('~')))+'\\AppData\\Local\\ConnectedDevicesPlatform\\'+'L.'+os.getlogin()+'\\ActivitiesCache.db'
    
    def engine():
        engine = create_engine('mysql+pymysql://root:msp21074a.@127.0.0.1/artifacts_v2.9', encoding='utf-8')
        return engine
    
    file_in = str(input_db)
    db = sqlite3.connect(file_in)
    cursor = db.cursor()

    #for the Activity table
    activityTable = get_activity(cursor)
    df_activityTable=pd.DataFrame(activityTable)
    index_list=[]
    idx=''
    for i in range(len(df_activityTable)):
        idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
        index_list.append(idx)
        mac_addr=MAC_addr
      
    df_activityTable.insert(loc=0, column='MAC_addr', value=mac_addr)
    df_activityTable.insert(loc=0, column='idx', value=index_list)
    df_activityTable.columns=['idx','MAC_addr','Last Modification Time', 'Expiration Time', 'Last Modification Time on Client', 'Start Time', 'Time Created in Cloud', 'ETag', 'Application', 'Display Name', 'Display Text', 'Activity Type', 'Activity Status', 'Priority', 'Is Local Only', 'Tag', 'Group', 'Match ID', 'Platform', 'Description', 'Content Uri', 'App Activity ID', 'Parent Activity ID', 'Platform Device ID', 'Dds Device ID', 'Clipboard Data ID', 'Clipboard Data', 'GDPR Type', 'Package ID Hash', 'Original Payload']
    df_activityTable.to_sql('win10_activity', con=engine(),if_exists='append',index=False)
    
     #for the packageID
    packageID = get_packageID(cursor)
    df_packageID=pd.DataFrame(packageID)
    index_list=[]
    idx=''
    for i in range(len(df_packageID)):
        idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
        index_list.append(idx)
        mac_addr=MAC_addr
    df_packageID.insert(loc=0, column='MAC_addr', value=mac_addr)
    df_packageID.insert(loc=0, column='idx', value=index_list)  
    df_packageID.columns=['MAC_addr','idx','Activity ID', 'Platform', 'Package Name', 'Expiration Time']
    df_packageID.to_sql('win10_packageid', con=engine(),if_exists='append',index=False)

    db.close()


#=
# get the basic information 
def getIPList():
    ipList=[]
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in addrs:
        if ':' not in item[4][0]:
            ipList.append(item[4][0])
    iplist=str(ipList)
    return iplist

# get the basic information 
def basic_infor():

    ip_addr=getIPList()
    w = wmi.WMI()
    pc_infor=[]
    
    for CS in w.Win32_ComputerSystem():
        pc_infor.append(CS.Caption)
        pc_infor.append(CS.UserName)
        pc_infor.append(CS.Manufacturer)
        pc_infor.append(CS.Workgroup)
        pc_infor.append(CS.model)
    for OS in w.Win32_OperatingSystem():
        pc_infor.append(OS.Caption)
        pc_infor.append(OS.OSArchitecture)
    
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0)
    #####print ("OS VERSION : " + winreg.QueryValueEx(key,"ProductName")[0])
    #####print ("Detailed VERSION : " + winreg.QueryValueEx(key,"BuildLabEx")[0])
    #####print ("USER : " + winreg.QueryValueEx(key,"RegisteredOwner")[0])
    a=winreg.QueryValueEx(key,"ProductName")[0]
    b=winreg.QueryValueEx(key,"BuildLabEx")[0]
    c=winreg.QueryValueEx(key,"RegisteredOwner")[0]
    winreg.CloseKey(key)


    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\ControlSet001\\Control\\Windows", 0)
    #####print ("Last_ShutDown_Time : ",end="")
    date = winreg.QueryValueEx(key,"ShutdownTime")[0].hex()
    strdate = date[-2:] + date[-4:-2] + date[-6:-4] + date[-8:-6] + date[-10:-8] + date[-12:-10] + date[-14:-12] + date[-16:-14]
    dateint = int(strdate,16)
    us = dateint / 10.
    #####print(datetime(1601,1,1)+ timedelta(microseconds=us))
    i=1
    from datetime import datetime,timedelta
    d=datetime(1601,1,1)+ timedelta(microseconds=us)
    winreg.CloseKey(key)
    idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
    sql="""insert into basic_infor(idx,MAC_addr,ip_addr,OS_VERSION,Detailed_VERSION,USER,Last_ShutDown_Time, PC_Name, Username, PC_manufa, Workgroup, Model, OS_name , OS_arch) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    curs.execute(sql,(idx,MAC_addr,ip_addr,a,b,c,d,pc_infor[0],pc_infor[1],pc_infor[2],pc_infor[3],pc_infor[4],pc_infor[5],pc_infor[6]))
    conn.commit()
    

# The following codes refer to https://github.com/uwol1116/artifact_collector
def Iconcache(): 
    #filename='C:/Users/cysun/AppData/Roaming/Microsoft/Windows/Recent/002.gif.lnk'
    USERNAME=os.environ['USERNAME']
    filename="C:/Users/"+USERNAME+"/AppData/Local/IconCache.db"
    tmp=""
    tmp2=""
    list=[]
    path=[]
    list_of_full_path=[]
    list_of_full_path22=[]
    list_of_full_path33=[]
    list_of_full_path44=[]
    
    def find_path(st,end):
        convert_path=""
        ggggg=0
        for q in range(st,end,2):
            if (tmp2[q]== " "):
                ggggg+=1
            else:
                convert_path+=tmp2[q]
        return(convert_path)
        
    fd=open(filename,'rb')
    ##print ("size : "+str(os.path.getsize(filename)))
    for i in range(1,os.path.getsize(filename)+1):
        data=fd.read(1)
        if (ord(data)>=16):
            tmp += str(hex(ord(data))[2:])
            tmp2+=chr(ord(data))
        else:
            tmp += str('0')
            tmp += str(hex(ord(data))[2:])
            tmp2+=chr(ord(data))


    lenn=len(tmp)

    for i in range(0,lenn,2):
        temp=""
        temp+=tmp[i]
        temp+=tmp[i+1]
        list.append(temp)

    count=0
    try:
            for j in range(0,os.path.getsize(filename)-10000,1):
                ##print (list[j])
                if (list[j]=='63' and list[j+2]=='3a'): 
                    ##print(j)
                    for k in range(200):
                        ##print(list[j+k])
                        if(list[j+k]=='ff' and list[j+k+1]=='ff' and list[j+k+2]=='ff'):
                            path.append((j,j+k-1))
                            count+=1
                            break;
    except IndexError :
            print("err")

    fd.close()

    cnt=1
    for x in range (count-1):
        full_path=""
        full_path=find_path(path[x][0],path[x][1])
        ##print(full_path)
        list_of_full_path.append(full_path)
        #sql="""insert into IconCache(idx,Path) values (%s,%s)"""
        #curs.execute(sql,(cnt,full_path,))
        #conn.commit()
        cnt+=1
    ##print(list_of_full_path)
    for x in list_of_full_path:
            lengthh=len(x)
            aa=""
            for y in range(lengthh):
                    aa+=x[y]
                    #if(x[y]="." and x[y+1]="d" and x[y+2]="l" and x[y+3]="l"):
                    if(x[y]=="."):
                            if(x[y+1]=="d"):
                                    aa+="dll"
                                    break
                            elif(x[y+1]=="e"):
                                    aa+="exe"
                                    break
                            elif(x[y+1]=="c"):
                                    aa+="cpl"
                                    break
                            elif(x[y+1]=="l"):
                                    aa+="lnk"
                                    break
                            elif(x[y+1]=="i"):
                                    aa+="ico"
                                    break
            ##print(aa)
            list_of_full_path22.append(aa)
    
    ccnntt=1
    ##print(type(list_of_full_path22))
    list_of_full_path33 = collections.OrderedDict.fromkeys(list_of_full_path22).keys()
    for z in list_of_full_path33:
            idx=md5_mac_addr[:7]+collect_time+'-'+str(ccnntt)
            sql="""insert into IconCache(idx,MAC_addr,Path) values (%s,%s,%s)"""
            curs.execute(sql,(idx,MAC_addr,z,))
            conn.commit()
            ccnntt+=1


# get the event log
def eventlog(evtx_type):
    server = 'localhost' # name of the target computer to get event logs
    logtype=str(evtx_type)
    table_name=logtype

    if(logtype=='Windows Powershell'):
        table_name='windows_powershell'
    if(logtype=='Microsoft-Windows-Store%4Operational'):
        table_name='store_operational' 
    if(logtype=='Microsoft-Windows-PowerShell%4Operational'):
        table_name='powershell_operational'
    if(logtype=='Microsoft-Windows-AppXDeploymentServer%4Operational'):
        table_name='appx_operational'
    if(logtype=='Microsoft-Windows-GroupPolicy%4Operational'):
        table_name='grouppolicy_operational'
    if(logtype=='Microsoft-Windows-Ntfs%4Operational'):
        table_name='ntfs_operational'
   
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)  
    i=1
    print('Collecting the %s eventlog, the Processing are as follows:' % logtype )
    while True:
        events = win32evtlog.ReadEventLog(hand, flags,0)
        if events:
            for event in events: 
                #print(event)
                if (i<100000):  ###################################################갯수조절###################3########     i    로 ##########
                        #print('Collecting the eventlog, the Processing as follows:')
                        print('\r'+'█'*((int((i/total)*100)))+'Current Process:{}%'.format(int((i/total)*100)),end='',)    #print()
                        data = event.StringInserts
                        #print(data)
                        if data:
                            ##print ('Event Data:')
                            f = ""
                            for msg in data:
                                f += str(msg)
                                f += "\n"
                            #print(f)
                        a=event.EventCategory            
                        b=str(event.TimeGenerated)
                        c=event.SourceName
                        d=event.EventID
                        e=event.EventType
                        #print(c)
                        idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
                        #f1=f
                        sql="""insert into evtx_%s""" % table_name + """(idx,Event_Category,Time_Generated,Source_Name,Event_ID,Event_Type,Event_Data) values (%s,%s,%s,%s,%s,%s,%s)"""                        
                        curs.execute(sql,(idx,a,b,c,d,e,f,))
                        conn.commit()
                        #print(i)
                        i+=1
                        ##print('*' * 100)   
        else:
            break

def UserAssist():
    varReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    varKey = winreg.OpenKey(varReg, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\\Count",0, winreg.KEY_ALL_ACCESS)
    #key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\\Count',0, winreg.KEY_ALL_ACCESS)
    intab = "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz"
    outtab = "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
    rot13 = str.maketrans(intab,outtab)
    try:
        i = 0
        while True:
            SessionNumber = ""
            RunCount = ""
            LastRunTime = ""
            name, value, type = winreg.EnumValue(varKey,i)
            #####print (name.translate(rot13))
            text1 = value
            for j in range(0,8):
                SessionNumber += binascii.hexlify(text1).decode()[j]
            SessionUnpack = SessionNumber[-2:] + SessionNumber[-4:-2] + SessionNumber[-6:-4]+SessionNumber[-8:-6]
                    
            for j in range(8,16):
                RunCount += binascii.hexlify(text1).decode()[j]
            RunUnpack = RunCount[-2:] + RunCount[-4:-2] + RunCount[-6:-4]+RunCount[-8:-6]

            for j in range(120,136):
                LastRunTime += binascii.hexlify(text1).decode()[j]
            LastRunUnpack = LastRunTime[-2:] + LastRunTime[-4:-2] + LastRunTime[-6:-4] + LastRunTime[-8:-6] + LastRunTime[-10:-8] + LastRunTime[-12:-10] + LastRunTime[-14:-12] + LastRunTime[-16:-14]
            lastint = int(LastRunUnpack,16)
            us = lastint / 10.
            ##print(datetime(1601,1,1)+ timedelta(microseconds=us))
            
            #####print("Session Number : " + str(SessionUnpack) + " Run Count : " + str(RunUnpack) + " Last Run Time : " + str(datetime(1601,1,1)+ timedelta(microseconds=us)))
            #####print()

            a=name.translate(rot13)
            b=str(SessionUnpack)
            c=str(RunUnpack)
            from datetime import datetime,timedelta
            d=(datetime(1601,1,1)+ timedelta(microseconds=us))
            idx=md5_mac_addr[:7]+collect_time+'-'+str(i)
            #query="INSERT into registry_userassist VALUES (?,?,?,?,?)"
            sql="""insert into registry_userassist(idx,MAC_addr,Name,Session_Number,Run_Count,Last_Run_Time) values (%s,%s,%s,%s,%s,%s)"""
            curs.execute(sql,(idx,MAC_addr,a,b,c,d,))
            conn.commit()
            i += 1

    except WindowsError:
        pass

def AutoRun(): 
    caption = subprocess.getoutput('wmic startup get Caption').split("\n") 
    command = subprocess.getoutput('wmic startup get command').split("\n")
    count=1
   
    for i in range(1,len(caption)-2):
        if i % 2 == 0:
            a = caption[i]
            b = command[i]
            idx=md5_mac_addr[:7]+collect_time+'-'+str(count-1)
            sql="""insert into registry_autorun(idx,MAC_addr,caption,command) values (%s,%s,%s,%s)"""
            curs.execute(sql,(idx,MAC_addr,a,b,))
            conn.commit()
            count+=1
         ##print("caption : " + caption[i] + "command : " + command[i])

def USB(): #usb 
    varkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM",0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
    i = 0
    USB_Result = ""
    USB_User = ""

    while True:
        try:
            key = winreg.EnumKey(varkey,i)
            USB_Result += key
            i += 1

        except WindowsError:
            break

    USB_Result.split(',')
    fullname = len(USB_Result)
    index = USB_Result.find("ControlSet")
    USB_User = USB_Result[index+len("ControlSet"):index+len("ControlSet")+3]
    varkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\ControlSet"+USB_User+"\\Enum\\USB",0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

    #####print("USB, USBTOR INFO")
    try:
        i = 0
        while True:
            device = winreg.EnumKey(varkey,i)
            #####print(device)
            a=str(device)
            idx=md5_mac_addr[:7]+collect_time+'-'+str(i+1)
            sql="""insert into registry_usbname(idx,MAC_addr,USB_Name) values (%s,%s,%s)"""
            curs.execute(sql,(idx,MAC_addr,a,))
            conn.commit()
            i += 1

    except WindowsError:
        pass
     
    #####print()
    #####print("List of connected devices")
    try:
        varkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\\Microsoft\\Windows Portable Devices\\devices",0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        device_name = ""
        i = 0
        while True:
            device = winreg.EnumKey(varkey,i)
            device_name += device
            device_name += ":"
            i += 1
    except WindowsError:
        pass

    result = device_name.split(":")
    for i in range(0,len(result)-1):
        location_result = result[i] 
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows Portable Devices\\devices\\"+location_result, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
            #####print(winreg.QueryValueEx(key,'FriendlyName')[0])
            a=winreg.QueryValueEx(key,'FriendlyName')[0]
            #####print(result[i])
            b=result[i] 
            idx=md5_mac_addr[:7]+collect_time+'-'+str(i+1)
            sql="""insert into registry_conn_device(idx,MAC_addr,Connected_devices_name,specific_name) values (%s,%s,%s,%s)"""
            curs.execute(sql,(idx,MAC_addr,a,b,))
            conn.commit()

def get_language():
    dll_handle = ctypes.windll.kernel32
    sys_lang = hex(dll_handle.GetSystemDefaultUILanguage())
    return sys_lang
    
def Registry_Wireless(): 
                #table = network column = name, password 필요
    if(get_language()=='0x409'):
        Nlist = subprocess.getoutput("netsh wlan show profile").split("All User Profile :")
        keyword='Key Content'
    if(get_language()=='0x804'):
        Nlist = subprocess.getoutput("netsh wlan show profile").split("所有用户配置文件 :")
        keyword='关键内容'
    b=""
    count = 1
    while count < len(Nlist):
        name = Nlist[count].strip()
        ####print("name : " + str(name)) 
        a=str(name)
        profile = subprocess.getoutput("netsh wlan show profile " + str(name) + " key=clear").split()
        for i in range(len(profile)):
            if keyword in profile[i]:
                ####print("password : "+ str(profile[i+2]))
                b=str(profile[i+2])
        idx=md5_mac_addr[:7]+collect_time+'-'+str(count)
        sql="""insert into registry_wireless(idx,MAC_addr,Name,Password) values (%s,%s,%s,%s)"""
        curs.execute(sql,(idx,MAC_addr,a,b,))
        conn.commit()
        count += 1

def show_process_fake():
     for i in range(101):
        time.sleep(0.01)
        print('\r'+'█'*((int((i))))+'Current Process:{}%'.format(int((i))),end='',flush=True)


if __name__ == "__main__":

    # run the function which need the admin privileges
    #def acquired_with_admin() :
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        # place the function which need to run in admin mode 
        print()
        print('[These operation are in the Administrator mode:]')
        print()
        #print()
      
        USB_User = ""
        MAC_addr=GetMAC()
        md5_mac_addr = hashlib.md5(MAC_addr.encode('utf8')).hexdigest()

        print(msp21074_logo)

        try:
            conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='msp21074a.',db='artifacts_v2.9')
            #conn = pymysql.connect(host='192.168.43.128',user='root',password='07cc24',db='cysun31')
            curs=conn.cursor()
            print()
            print("[Remote Server Connected Successfuly!]")
            #print()
        except Exception as err:
            print('The Network Connection is Error')
            print()
            print("Press 'D' to exit...")
            while True:
                if ord(msvcrt.getch()) in [68, 100]:
                    break
    
        print()
        print("The Collecting job is working, the following is the processing:")
        print()


        sql = """
            create table if not exists basic_infor(idx varchar(40) not null, MAC_addr varchar(40), Ip_addr varchar (100), OS_VERSION varchar(200), Detailed_VERSION varchar(90), USER varchar(100), Last_ShutDown_Time varchar(200), PC_Name varchar(40), Username varchar(40), PC_manufa varchar(40), Workgroup varchar(40), Model varchar(40), OS_name varchar(40), OS_arch varchar(40), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()
        
        sql = """
            create table if not exists IconCache( idx varchar(40) not null, MAC_addr varchar(40), Path varchar(200) not null, primary key (idx));
            """
        curs.execute(sql)
        conn.commit()


        sql = """
            create table if not exists evtx_system ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()
                   
        sql = """
            create table if not exists evtx_security ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists evtx_application ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)

        conn.commit()

        sql = """
            create table if not exists evtx_windows_powershell( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()
    
        sql = """
            create table if not exists evtx_store_operational ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()
        
        sql = """
            create table if not exists evtx_powershell_operational ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists evtx_appx_operational ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists evtx_grouppolicy_operational ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists evtx_ntfs_operational ( idx varchar (40) not null, Event_Category integer(20) not null, Time_Generated varchar(25) not null, Source_Name varchar(100) not null, Event_ID integer(20),Event_Type integer(20) , Event_Data varchar(10000), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()


        sql = """
            create table if not exists registry_userassist(idx varchar(40) not null, MAC_addr varchar(40), Name VARCHAR(200) not null, Session_Number VARCHAR(10), Run_Count VARCHAR(10), Last_Run_Time VARCHAR(30) , primary key(idx));;
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists registry_autorun(idx varchar(40) not null, MAC_addr varchar(40), caption varchar(200), command varchar(200), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        sql = """
            create table if not exists registry_usbname(idx varchar(40) not null, MAC_addr varchar(40), USB_Name varchar(200), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit() 

        sql = """
            create table if not exists registry_conn_device(idx varchar(40) not null, MAC_addr varchar(40),  Connected_devices_name varchar(200),specific_name varchar(200),time varchar(20),primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        #create table
        sql = """
            create table if not exists registry_wireless( idx varchar(40) not null, MAC_addr varchar(40), Name varchar(30), Password varchar(80), primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()   
        
        #create table for prefetch 
        sql = """
            CREATE TABLE IF NOT EXISTS prefetch (idx VARCHAR ( 40 ) NOT NULL, MAC_addr varchar(40), Pf_name varchar (1000), EXE_name varchar(100), Run_count varchar(10), last_run varchar(500), Vol_0_name varchar(100), Vol_0_create_T varchar(50), Vol_0_SN varchar(40), Vol_1_name varchar(100), Vol_1_create_T varchar(50), Vol_1_SN varchar(40), Directory_Strings LONGTEXT, Resources LONGTEXT, primary key (idx) );
            """
        curs.execute(sql)
        conn.commit()

        #create table for recycle_bin
        sql = """
            CREATE TABLE IF NOT EXISTS recycle_bin (idx VARCHAR ( 40 ) NOT NULL, MAC_addr varchar(40), deleted_date VARCHAR ( 40 ), file_type VARCHAR ( 20 ), file_size VARCHAR ( 20 ), file_path VARCHAR ( 200 ), file_name VARCHAR ( 100 ), ifile_name VARCHAR ( 200 ), rfile_name VARCHAR ( 200 ));
            """
        curs.execute(sql)
        conn.commit()
        
        # run the function 
        # get the basic information
        
        basic_infor()
        print("Collecting and Parsing the Basic Information!")
        show_process_fake() 
        print('\n')    
        
        # get the iconcache
        Iconcache()
        print("Collecting and Parsing the Iconcache Information!")
        show_process_fake()
        print('\n') 
        
        # get the registry information of UserAssist
        UserAssist()
        AutoRun()
        USB()
        Registry_Wireless()
        print("Collecting and Parsing the UserAssist, Autorun, USB, & Wireless Information!")
        show_process_fake()  
        print('\n')
        # get the registry information of Autorun 

        eventlog('system')
        print('\n')
        eventlog('application')
        print('\n')
        eventlog('security') 
        print('\n')

        eventlog('Windows Powershell')
        print('\n')
        eventlog('Microsoft-Windows-Store%4Operational')
        print('\n')
        eventlog('Microsoft-Windows-PowerShell%4Operational')
        print('\n')
        eventlog('Microsoft-Windows-AppXDeploymentServer%4Operational')
        print('\n')
        eventlog('Microsoft-Windows-GroupPolicy%4Operational')
        print('\n')
        eventlog('Microsoft-Windows-Ntfs%4Operational')
        print('\n')
        
        jumplist = JL()
        print("Collecting and Parsing the Lnk & Jumplist Information!")
        show_process_fake() 
        print('\n')
         
        parsed_Prefetch()
        print("Collecting and Parsing the Prefetch Information!")
        show_process_fake() 
        print('\n')

        parsed_Recyclebin()
        print("Collecting and Parsing the $Recycle_Bin Information!")
        show_process_fake() 
        print('\n')
        

        print()
        print()   
        print("The Collection work done! Press 'D' to exit...")
        while True:
            if ord(msvcrt.getch()) in [68, 100]:
                break    
                sys.exit(0)
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)



