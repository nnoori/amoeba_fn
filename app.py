
from collections import defaultdict
from logging import basicConfig, DEBUG
from user_management.session_management import UserSession
from user_management.user import app_user_management, get_render

import web

import config


VERSION = "0.0.1"

urls = (
    '/', 'Index',
     '/user', app_user_management,
    '/logout', 'Main',
    '/about', 'About',
    '/book_shelf', 'Book_Shelf',
    '/contacts', 'Contacts'
    )

app = web.application(urls, globals())

# Allow session to be reloadable in development mode.
if web.config.get('_session') is None:
    store   = web.session.DiskStore('sessions')
    session = UserSession(app, store, initializer = \
                      {'login': 0, 'username': '', 'user_type': 0})        


    #session = web.session.Session(app, web.session.DiskStore('sessions'),
    #                              initializer={'flash': defaultdict(list)})

    web.config._session = session
else:
    session = web.config._session

def add_flash(group, message):
    session.flash[group].append(message)
def flash_messages(group=None):
    if not hasattr(web.ctx, 'flash'):
        web.ctx.flash = session.flash
        session.flash = defaultdict(list)
    if group:
        return web.ctx.flash.get(group, [])
    else:
        return web.ctx.flash

# Setup global template functions
t_globals = dict(
    datestr=web.datestr,
    app_version=lambda: VERSION + ' - ' + config.env,
    flash_messages=flash_messages,
    )

render_partial = web.template.render('templates/', cache=config.cache,
                                     globals=t_globals)
# Allow rendering of partials in partials
render_partial._keywords['globals']['render'] = render_partial

render = web.template.render('templates/',
                             base='base',
                             cache=config.cache,
                            globals=t_globals)
# Allow rendering of partials
render._keywords['globals']['render'] = render_partial
#render = web.template.render('templates/')

class Index:
    
    def GET(self, name=''):
        render = get_render()
        return render.index()

    #def GET(self):
    #    return render.index()

# class Main:
#     def GET(self):
#         return render.main()

# class Login:
#     def GET(self):
#         return render.login()

# class Create:
#     def GET(self):
#         return render.create()

class About:
    def GET(self):
        return render.about()

class Book_Shelf:
    def GET(self):
        return render.book_shelf()

class Account:
    def GET(self):
        return render.account()
class Contacts:
    def GET(self):
        return render.contacts()


# Set a custom internal error message
def internalerror():
    msg = """
    An internal server error occurred. Please try your request again by hitting back on your web browser. You can also <a href="/"> go back to the main page.</a>
    """
    return web.internalerror(msg)


# Setup the application's error handler
app.internalerror = web.debugerror if web.config.debug else internalerror

if config.email_errors:
    app.internalerror = web.emailerrors(config.email_errors,
                                        app.internalerror,
                                        'server-error@example.com')


# Adds a wsgi callable for uwsgi
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
