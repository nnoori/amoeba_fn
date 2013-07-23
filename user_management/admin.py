''' This file contains the routines that would be 
handling administrator operations
'''
from database_management import UserDatabase
from logging import getLogger
from util.config import USER_TYPES
#import user_management.admin as app_admin
import web
from web import form

LOGGER = getLogger(__name__)

#web.config.debug = False                            # Required for sessions

urls = (
    '/list_user',      'list_user', # Admin dashboard 
    '/add_user',       'add_user', #Add user account
    '/delete_user',    'delete_user', #delete usr account
    '/user',           'user' # view user account
)

app_admin_management = web.application(urls, globals())
#database = UserDatabase()
#database.setup_database()

class add_user:
   
    def GET(self):
        
        render = get_render('admin')
        return render.add_user()
       
class delete_user:
    
    def GET(self):
       
	    render = get_render('admin')
	    return render.delete_user()
        
class list_user:

    def GET(self):
                
        render = get_render('admin')
        return render.list_user()
        
class user:

    def GET(self):
        '''
        The login_again.
        '''
        
        render = get_render('admin')
        return render.user()

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