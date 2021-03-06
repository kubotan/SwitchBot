#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 【注意】近接するSwitchBotのMACアドレスを検索するプログラムですが
# お隣のも拾う可能性があるので、電池を抜いた場合に反応しないかなどで
# 確認してください。
# apt-get install python3-pip
# pip3 install bluepy
# chmod 755 ./search_mac_addr.py
# ./search_mac_addr.py

from bluepy import btle

UUID_SERVICE='cba20d00-224d-11e6-9fb8-0002a5d5c51b'

if __name__ == '__main__': 
  index = 0   # 0=/dev/hci0
  timeout = 3.0
  scanner = btle.Scanner(index)
  devices = scanner.scan(timeout)

  print('SwitchBot list:') 
  for dev in devices:
    for (adTypeCode, desc, value) in dev.getScanData():
      if adTypeCode == 7 and value == UUID_SERVICE:
        print(f'  MAC address={dev.addr}, Type={dev.addrType}, RSSI={dev.rssi} dB')
