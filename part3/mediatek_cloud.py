# Copyright (C) HENNES CO., LTD. - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written in May 2016 by
# Li-Wei Shih
# Hao-Yun Hsueh
# Feng-Chih Hsu
# Hsiang-Jiu Lin
# Cheng-Chang Liu
# Pei-Hsuan Yan
import socket
import logging
import httplib
import json
import config

def send_data_point(dev_id, dev_key, data_id, data_value):
    http_client = httplib.HTTPConnection('api.mediatek.com')

    url = '/mcs/v2/devices/%s/datapoints.csv' % dev_id
    headers = {'deviceKey': dev_key}
    body = '%s,,%s' % (data_id, data_value)
    http_client.request('POST', url, body=body, headers=headers)

def receive_data_point(dev_id, dev_key, data_id):
    http_client = httplib.HTTPConnection('api.mediatek.com')

    url = '/mcs/v2/devices/%s/datachannels/%s/datapoints' % (dev_id, data_id)
    headers = {'deviceKey': dev_key}
    http_client.request('GET', url, headers=headers)

    response = http_client.getresponse()
    result = json.loads(str(response.read(), 'UTF-8'))
    return result

def set_house_status(status):
    try:
        send_data_point(config.DEVICE_ID, config.DEVICE_KEY, config.CHANNEL_STATUS_ID, status)
    except Exception:
        logging.warning('cannot connect to MediaTek Cloud service')
        return
