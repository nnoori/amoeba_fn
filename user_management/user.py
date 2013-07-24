'''
This is the main routine of the web-app.  It is responsible for addressing,
parameters.session construction/storage, and basic page logic. 

Created on Nov 8, 2011
@author: andrewnelder
'''

from database_management import UserDatabase
from logging import getLogger
from util.config import USER_TYPES

import web
from web import form

LOGGER = getLogger(__name__)

#web.config.debug = False                            # Required for sessions

urls = (
    '/login',          'login',
    '/logout',         'logout',
    '/create',         'create_user',
    '/delete',         'delete_user',
    '/login_again',    'login_again', 
    '/profile', 'profile'
    
)
app_user_management = web.application(urls, globals())
database = UserDatabase()
database.setup_database()

 #=================================
vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
form.Textbox("username", description="Username", value=''),
form.Textbox("email", vemail, description="E-Mail",value=''),
form.Password("password", vpass, description="Password",value=''),
form.Password("password2", description="Repeat password",value=''),
form.Button("submit", type="submit", description="Register",value=''),
validators = [
    form.Validator("Passwords did't match", lambda i: i.password == i.password2)]
)
        #=================================
class create_user:
   
    def GET(self):
        '''
        Create User Form
        '''
        f = register_form()
        render = get_render()
        return render.user.create(f)
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        #username = web.input().username
        #password = web.input().password
        #email    = web.input().email
        f = register_form()
        
        if not f.validates():
            page = web.seeother('/not_found')
            return page
        else:
            create_success = \
            database.create_user(f['username'].value, f['password'].value, f['email'].value)
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
        print user_type
        web.ctx.session.attempt_login(username, user_type)
        if web.ctx.session.is_logged():
            if user_type is USER_TYPES['admin']:

                print 'User is logged as administrator'
                # redirect user to 'administration' page
                page = web.redirect('../admin/list_user')
            elif user_type is USER_TYPES['user']: 
                print 'User is logged as a regular user'
                #redirect the user to the 'user profile' page
                #page = web.redirect('/profile')
                render = get_render()
                return render.profile(username)
        else:
            #user is not logged for some reason - 
            #redirect to login again until we figure the error pages
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

class profile:

    def GET(self,username=''):

        #Check is user is logged in to view profile 
        render = get_render()
        return render.user.profile()

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