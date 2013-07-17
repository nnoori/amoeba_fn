'''
Created on Nov 13, 2011
@author: andrewnelder
'''

from logging import basicConfig, DEBUG
from user_management.session_management import UserSession
from user_management.user import app_user_management, get_render
import web

urls = (
    '/user',                app_user_management,
    '/admin',               'admin',
    '/',                'index',
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
        render = get_render()
        return render.index()

class admin:
    
    def GET(self):
        if web.ctx.session.is_admin():
            render = get_render('admin')
            page = render.admin()
        else:
            page = web.seeother('/')
        return page

class About:
    def GET(self, name=''):
        render = get_render('temp')
        return render.about()

class Book_Shelf:
    def GET(self):
        render = get_render('temp')
        return render.book_shelf()

class Account:
    def GET(self):
        render = get_render('temp')
        return render.account()
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

if __name__ == '__main__':
    basicConfig(level=DEBUG)
    app.run()