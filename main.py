import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path
import pymongo
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=0, help="1:watch in real time (debug mode)", type=bool)

class Application(tornado.web.Application):
  def __init__(self):
    conn = pymongo.Connection('localhost', 27017)
    self.db = conn.links

    handlers = [
      (r"/", IndexHandler),
    ]
    settings = dict(
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "assets"),
      debug=options.debug,
    )
    tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    db = self.application.db
    items = {}
    tags = ['algorithm', 'android', 'javascript', 'design',
      'go', 'note', 'infrastructure', 'ios/osx',
      'mongodb', 'mysql', 'python', 'research',
      'ruby', 'data-science', 'tips']

    for tag in tags:
      items_in_tag = []
      items_raw = db.links.item.find({'tag':tag})
      for item in items_raw:
        del item['_id']
        items_in_tag.append(item)
      items.update({tag:items_in_tag})

    self.render('index.html', items=items)

if __name__ == "__main__":
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
