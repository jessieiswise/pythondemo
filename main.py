import sys
import os
sys.path.append( os.path.dirname(__file__) +  'libs/' )

from flask import Flask, render_template, make_response, request, Response, send_from_directory
app = Flask(__name__, static_url_path='')
import json
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()




class base_handler():
    def setDefaultCache(self):
        default_dict = {
            'name':'jessica',
            'message':'hi! this is a test post!'
        }
        cache.add('0',default_dict)
        cache.set('postCount',1)


class routing_handler(base_handler):
    def warm_up(self):
        self.setDefaultCache()
        app.add_url_rule('/static/<path:path>', 'stc', self.staticFiles)
        app.add_url_rule('/', 'home',self.home)
        app.add_url_rule('/add', 'post',self.newEntry)
        app.add_url_rule('/get', 'get',self.getEntries)
        app.run()
    def staticFiles(self,path):
        return send_from_directory('static',path)
    def home(self):
        return render_template('main.html')
    def newEntry(self):
        #didnt bother to do any sanity/security checks here. Use at your own risk.
        data = request.json
        data_formmatted = json.loads(data)
        try:
            current_count = cache.get('postCount')
            cache.add(str(current_count + 1),data)
            cache.set('postCount',str(current_count + 1))
        except Exception as e:
            print(e)
            return json.dumps({'status':'failed'})
    def getEntries(self):
        response = []
        number_of_posts = cache.get('postCount')
        post_iterator = range(number_of_posts)
        for n in post_iterator:
            response.append(cache.get(str(n)))
        if response != []:
            return json.dumps({'status':'success','payload':response})
        else:
            return json.dumps({'status':'failed'})

if __name__ == '__main__':
    rtr = routing_handler()
    rtr.warm_up()
