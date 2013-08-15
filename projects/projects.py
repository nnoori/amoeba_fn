
#from user_management.database_management import UserDatabase
from logging import getLogger
from util.config import USER_TYPES

import web
from web import form

LOGGER = getLogger(__name__)

#web.config.debug = False                            # Required for sessions

urls = (
    '/create_project', 'create_project',
    '/delete_project', 'delete_project',
    '/create_book',    'create_book',
    '/delete_book',    'delete_book',
    '/project_list',   'project_list'
    
)
app_project_management = web.application(urls, globals())
#database = UserDatabase()
#database.setup_database()

 #=================================
#vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
#vemail = form.regexp(r".*@.*", "must be a valid email address")

project_form = form.Form(
form.Textbox("project_name", description="Project Name", value=''),
form.Textbox("book_title", description="Book title",value=''),
form.Button("submit", type="submit", description="Create book",value=''),
)
        #=================================
class create_project:
   
    def GET(self):
        '''
        Create project Form
        '''
        f = project_form()
        render = get_render()
        return render.project.create_project(f)
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        #username = web.input().username
        #password = web.input().password
        #email    = web.input().email
        #f = project_form()
        
        page = web.seeother('/create_book')
            
        return page

class delete_project:
    
    def GET(self):
        '''
        Delete user form.
        '''
        render = get_render()
        return render.delete_project()
    
    def POST(self):
        
        name = web.input().project_name
        title = web.input().book_title
        
        page = web.seeother('/delete_book')
        
        return page

class create_book:

    def GET(self):
        render = get_render()
        return render.create_book()

class delete_book:

    def GET(self):
        render = get_render()
        return render.delete_book()

class project_list:

    def GET(self):
        render = get_render()
        return render.project_list()



def get_render(template='project'):
    
    render = web.template.render('templates/common/project', \
                                base='base_project', \
                                globals={'context': web.ctx.session})
    return render