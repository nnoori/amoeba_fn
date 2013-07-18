'''
This is the main routine of the web-app.  It is responsible for addressing,
parameters.session construction/storage, and basic page logic. 

Created on Nov 8, 2011
@author: andrewnelder
'''

from database_management import UserDatabase
from logging import getLogger
import web

LOGGER = getLogger(__name__)

#web.config.debug = False                            # Required for sessions

urls = (
    '/login',          'login',
    '/logout',         'logout',
    '/create',         'create_user',
    '/delete',         'delete_user',
    '/login_again',    'login_again' 
)
app_user_management = web.application(urls, globals())
database = UserDatabase()
database.setup_database()

class create_user:

    def GET(self):
        '''
        Create User Form
        '''
        
        render = get_render()
        return render.user.create()
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        
        username = web.input().username
        password = web.input().password
        email    = web.input().email
        
        create_success = \
            database.create_user(username, password, email)

        # if successful then login_ok.html else login_error.html 
        if create_success:
            page = web.seeother('/login')
        else:
            page = web.seeother('/create')
        
        return page

class delete_user:
    
    def GET(self):
        '''
        Delete user form.
        '''
        render = get_render()
        return render.user.delete()
    
    def POST(self):
        
        username = web.input().username
        password = web.input().password
        
        success = database.delete_user(username, password)
        
        if success:
            page = web.seeother('/logout')
        else:
            page = web.seeother('/delete')
        
        return page

class login:

    def GET(self):
        '''
        The login form.
        '''
        
        render = get_render()
        return render.user.login()
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        
        username = web.input().username
        password = web.input().password
        
        # determine if username and password are correct
        user_type = database.attempt_login(username, password)
        if user_type:
            print 'User name and password are correct'
            web.ctx.session.attempt_login(username, user_type)
        else: 
            print 'user name and password are not correct'
        # if successful then login_ok.html else login_error.html 
        if web.ctx.session.is_logged():
            # TODO: Wrong page?
            page = web.redirect('../')
        else:
            page = web.seeother('/login_again')
        
        return page

class login_again:

    def GET(self):
        '''
        The login_again.
        '''
        
        render = get_render()
        return render.user.login_again()

class logout:
    
    def GET(self):
        web.ctx.session.logout()
        return web.redirect('../')

def get_render(template='common'):
    
    render = web.template.render('templates/common', \
                                base='base_user', \
                                globals={'context': web.ctx.session})
    if template is 'admin':
        render = web.template.render('templates/admin', \
                                    base='base_admin', \
                                    globals={'context': web.ctx.session})
    elif template is 'temp':
        render = web.template.render('templates/', \
                                    base='base_main', \
                                    globals={'context': web.ctx.session})
    elif template is 'index':
        render = web.template.render('templates/common', \
                                    base='base_index', \
                                    globals={'context': web.ctx.session})

    return render