#coding:utf-8

import urllib
import urllib2
import json
import time
import pymongo
from key import config

class PocketFetch:
  def __init__(self):
    conn = pymongo.Connection()
    self.db = conn.lists
    self.consumer_key = config.Pocket.consumer_key
    self.access_token = config.Pocket.access_token
    self.url = 'https://getpocket.com/v3/get'

  def saveItems(self, tag, since):
    params = {
      'consumer_key':self.consumer_key,
      'access_token':self.access_token,
      'tag':tag,
      'since': since
    }
    data = urllib.urlencode(params)
    req = urllib2.Request(self.url, data)
    res_raw = urllib2.urlopen(req).read()
    res = json.loads(res_raw)

    for r in res['list']:
      item = {
        'id':r,
        'title':res['list'][r]['resolved_title'].encode('utf_8'),
        'url':res['list'][r]['resolved_url']
      }
      self.db.lists.item.save(item)

def main():
  pocket = PocketFetch()
  since = int(time.time()) - 60 * 60 * 24
  tags = ['iOS', 'Android', 'Rails', 'Infrastructure']
  for tag in tags:
    pocket.saveItems(tag, since)

if __name__ == '__main__':
  main()