#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2017-present WonderLabs, Inc. <support@wondertechlabs.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# refs. https://github.com/OpenWonderLabs/python-host/
# refs. https://github.com/kanon700/python-host/

# apt-get install python3-pip
# pip3 install bluepy
# chmod 755 ./switchbot.py
# ./switchbot.py switch_on
# ./switchbot.py switch_off

import binascii
from bluepy import btle
import json
import requests
import sys
import traceback

MAC_ADDRESS='XX:XX:XX:XX:XX:XX'   # Check the Mac address of SwitchBot from the setting screen of the app.
COMMANDS = {
  'press'              : '5701',   # press mode
  'switch_on'          : '570101',   # switch mode
  'switch_off'         : '570102',   # switch mode
  'down'               : '570103',
  'up'                 : '570104',
  'show_settings'      : '5702',
  'set_reverse_off'    : '57036410',
  'set_reverse_on'     : '57036411',
  'set_long_press_0s'  : '570f0800',
  'set_long_press_1s'  : '570f0801',
  'set_long_press_2s'  : '570f0802',
  'set_long_press_3s'  : '570f0803',
  'set_long_press_4s'  : '570f0804',
  'set_long_press_5s'  : '570f0805',
  'set_long_press_10s' : '570f080a',
  'set_long_press_20s' : '570f0814',
  'set_long_press_30s' : '570f081e',
  'set_long_press_40s' : '570f0828',
  'set_long_press_50s' : '570f0832',
  'set_long_press_60s' : '570f083c',
}
EXIT_FAILURE=1
EXIT_SUCCESS=0
HANDLE_READ=0x13
HANDLE_WRITE=0x16
TIMEOUT_SECONDS_NOTIFICATIONS=1
UUID_SERVICE='cba20d00-224d-11e6-9fb8-0002a5d5c51b'
UUID_SPECIFIED_CHARACTERISTIC='cba20002-224d-11e6-9fb8-0002a5d5c51b'

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: ./switchbot (' + '|'.join(COMMANDS.keys()) + ')')
    sys.exit(EXIT_FAILURE)

  if sys.argv[1] not in COMMANDS:
    print('Unknown parameter.')
    sys.exit(EXIT_FAILURE)
  key=sys.argv[1]

  try:
    p = btle.Peripheral(MAC_ADDRESS, btle.ADDR_TYPE_RANDOM)
    p.waitForNotifications(TIMEOUT_SECONDS_NOTIFICATIONS)
    svc = p.getServiceByUUID(UUID_SERVICE)
    ch = svc.getCharacteristics(UUID_SPECIFIED_CHARACTERISTIC)[0]
    p.writeCharacteristic(HANDLE_WRITE, binascii.a2b_hex(COMMANDS[key]), True)
    value = p.readCharacteristic(HANDLE_READ)
    result = {}
    if key == 'show_settings':
      result['battery'] = value[1]
      result['firmware'] = value[2] / 10.0
      result['n_timers'] = value[8]
      result['dual_state_mode'] = bool(value[9] & 16)
      result['inverse_direction'] = bool(value[9] & 1)
      result['hold_seconds'] = value[10]
    else:
      result['return'] = binascii.b2a_hex(value).decode()
    print(str(result))
    p.disconnect()

  except Exception as e:
    print(traceback.format_exc())
    sys.exit(EXIT_FAILURE)

sys.exit(EXIT_SUCCESS)
