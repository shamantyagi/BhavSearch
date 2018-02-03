import random , os, os.path
import string
import redis, cherrypy
import jinja2
from operator import itemgetter

# jinja2 template renderer
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))


class bhavsearch(object):
    @cherrypy.expose
    def index(self):
				r=redis.StrictRedis(host="localhost",port=6379,db=0)
				search_results = r.scan(0,'*',10)
				search_detail = []		
				for stock in search_results[1]:
							temp = []
							temp.append(stock)
							temp_var = r.get(stock)
							temp.append( temp_var.split(',') )							
							search_detail.append(temp)
				search_detail=sorted(search_detail, key=itemgetter(0))
				tmpl = env.get_template('index.jinja')
				return tmpl.render(entries = search_detail)

    @cherrypy.expose
    def top_ten(self):
				r=redis.StrictRedis(host="localhost",port=6379,db=0)
				search_results = r.scan(0,'*',10)
				print len(search_results[1])
				search_detail = []		
				for stock in search_results[1]:
							temp = []
							temp.append(stock)
							temp_var = r.get(stock)
							temp.append( temp_var.split(',') )							
							search_detail.append(temp)
				print len(search_detail)
				search_detail=sorted(search_detail, key=itemgetter(0))
				print len(search_detail)
				tmpl = env.get_template('top_ten.jinja')
				return tmpl.render(entries = search_detail)

    @cherrypy.expose
    def generate(self, search=''):

				search=search.upper()	
				r=redis.StrictRedis(host="localhost",port=6379,db=0)
				search_results = r.keys('*'+search+'*')
				search_detail = []		
				for stock in search_results:
							temp = []
							temp.append(stock)
							temp_var = r.get(stock)
							temp.append( temp_var.split(',') )							
							search_detail.append(temp)
				tmpl = env.get_template('generate.jinja')
				return tmpl.render(stock_list = search_detail)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(bhavsearch(),'/',conf)
