'''
Created on Nov 13, 2011
@author: andrewnelder
'''

from logging import basicConfig, DEBUG
from user_management.session_management import UserSession
from user_management.user import app_user_management, get_render
from user_management.admin import app_admin_management
from projects.project import app_project_management 
 
import web

urls = (
    '/user',                app_user_management,
    '/admin',               app_admin_management,
    '/projects',             app_project_management,  
     '/',                   'index',
    '/about',               'About',
    '/book_shelf',          'Book_Shelf',
    '/contacts',            'Contacts'
)
app     = web.application(urls, globals())
store   = web.session.DiskStore('sessions')
session = UserSession(app, store, initializer = \
                      {'login': 0, 'username': '', 'user_type': 0})

class index:
    
    def GET(self, name=''):
        render = get_render('index')
        return render.index()

class About:
    def GET(self, name=''):
        render = get_render('temp')
        return render.about()

class Book_Shelf:
    def GET(self):
        render = get_render('temp')
        return render.book_shelf()

class Contacts:
    def GET(self):
        render = get_render('temp')
        return render.contacts()


# Sessions
def session_hook():
    print 'killed', session.is_expired()
    if session.is_expired():
        session.logout()
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))

# Configure HTTP error pages
htmlout = web.template.render( 'templates/')

def unauthorized( message='This page requires proper authorization to view.' ):
  result = { 'title':'401 Authorization Required', 'message':message }
  return web.unauthorized( htmlout.error( result ) )
app.unauthorized = unauthorized

def forbidden( message='Access is forbidden to the requested page.' ):
  result = { 'title':'403 Forbidden', 'message':message }
  return web.forbidden( htmlout.error( result ) )
app.forbidden = forbidden

def notfound( message='The server cannot find the requested page.' ):
  result = { 'title':'404 Not Found', 'message':message }
  return web.notfound( htmlout.error( result ) )
app.notfound = notfound

if __name__ == '__main__':
    basicConfig(level=DEBUG)
    app.run()