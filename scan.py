#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Scans countinously for cards and prints the UID
"""

__author__ = "Christoph Pranzl"
__version__ = "0.0.5"
__license__ = "GPLv3"

# rfid
from mfrc522_i2c import MFRC522 # gpl
import signal
# csv
import csv
import pprint
import os
# player
import subprocess
import time
import vlc
# switch
import RPi.GPIO as GPIO

continue_reading = True

# switch GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # stop
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # skip
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # play

# 0 : play
# 1 : pouse
# 2 : skip -> prev flag
Play_flag = 0 

def button_callback(channel):
    print(f'Pushed {channel}')

# Capture SIGINT for cleanup when script is aborted
def end_read(signal, frame):
    global continue_reading
    print('Ctrl+C captured, ending read')
    continue_reading = False

def play_flac(file_path):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()
    return player

def stop_music(player):
    player.stop()
    


def play_album(path):
    print(f'album list')
    file_names = os.listdir(path)
    play_list = []
    for name in file_names:
        print(f'{name}')
        tmp = path + '/' + name
        play_list.append(tmp)
    
    player = vlc.MediaListPlayer()
    mediaList = vlc.MediaList(play_list)
    player.set_media_list(mediaList) 
    player.set_playback_mode(vlc.PlaybackMode.loop) # looping
    #player.set_playback_mode(vlc.PlaybackMode.default) # 1 set
    player.play()
    f = True
    play_pause_flag = True # True : play , False : pause
    while f:
        b1 = GPIO.input(17)
        b2 = GPIO.input(26)
        b3 = GPIO.input(6)
        #print(f'b1 : {b1}, b2 : {b2}, b3 : {b3}')
        
        if b1 == 0:
            print('STOP')
            player.stop()
            time.sleep(1)
            break
        elif b2 == 0:
            print('skip')
            player.next()
            time.sleep(1)
        elif b3 == 0:
            print('play / pause')
            if play_pause_flag:
                print('pause')
                player.set_pause(1)
                play_pause_flag = False
            else:
                print('play')
                player.play()
                play_pause_flag = True
            time.sleep(1)
        time.sleep(0.05)


def callback(channel):
    print('button pushed %s'%channel)


if __name__ == '__main__':
    # read csv file uid:path
    uid_list = []
    with open('uid_list.csv') as f:
        reader = csv.reader(f)
        for line in reader:
            uid_list.append(line) 
        #print(f'{uid_list}')
    #print(f'1 uid:{uid_list[0][0]}, path:{uid_list[0][1]}')
    
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Reader is located at Bus 1, adress 0x28
    i2cBus = 1
    i2cAddress = 0x28

    # Create an object of the class MFRC522
    MFRC522Reader = MFRC522(i2cBus, i2cAddress)

    version = MFRC522Reader.getReaderVersion()
    print(f'MFRC522 Software Version: {version}')

    while continue_reading:
        # Scan for cards
        (status, backData, tagType) = MFRC522Reader.scan()
        if status == MFRC522Reader.MIFARE_OK:
            print(f'Card detected, Type: {tagType}')

            # Get UID of the card
            (status, uid, backBits) = MFRC522Reader.identify()
            if status == MFRC522Reader.MIFARE_OK:
                print('Card identified, UID: ', end='')
                uid_str = ''
                tmp = ''
                #print(f'{uid}')
                for i in range(0, len(uid) - 1):
                    print(f'{uid[i]:02x}:', end='')
                    tmp = format(uid[i],'02x')
                    uid_str = uid_str + tmp + ':'
                print(f'{uid[len(uid) - 1]:02x}')
                tmp = tmp = format(uid[len(uid) - 1],'02x')
                uid_str = uid_str + tmp
                print(f'uid_str : {uid_str}')

                # リスト参照してパス読み出し
                for line in uid_list:
                    if line[0] == uid_str:
                        print(f'Path ::: {line[1]}')
                        play_album(line[1])

