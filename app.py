import web
import client
from requests import codes
import _

urls = (
    r'/?', 'Home',
    r'/login/?', 'Login',
    r'/logout/?', 'Logout',
    r'/reg/?', 'Reg',
    r'/users/(\d+)/?', 'User',
    r'/users/(\d+)/edit/?', 'UserEdit',
)
app = web.application(urls, globals())

web.config.debug = True

session = None
if web.config.get('_session') is None:
    session = web.session.Session(app, 
        web.session.DiskStore('.sessions'), 
        initializer = {
             'user': {},
             'username': '',
             'message': '',
        }
    )
    web.config._session = session
else:
    session = web.config._session

def flash(message=None):
    if type(message) == str or type(message) == unicode:
        session.message = message
    elif type(message) == bool:
        message = session.message
        if message:
            session.message = None
        return message
    else:
        return session.message

class Home:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.dashboard()

class Login:        
    def GET(self):
        render = web.template.render('asset', base='before.common', globals=globals())
        return render.login()

    def POST(self):
        i = web.input()
        r, j = client.post('/login/', data=i)
        if r == codes.ok:
            session.user = j
            session.username = i.username
            raise web.redirect("/")
        else:
            flash(_.login.fail)
            raise web.redirect('/login/')

class Logout:
    def GET(self):
        session.user = {}
        session.username = ''
        session.message = ''
        session.kill()
        raise web.redirect("/")

class Reg:
    def GET(self):
        render = web.template.render('asset', base='before.common', globals=globals())
        return render.register()
    def POST(self):
        i = web.input()
        r, j = client.post('/users/')
        if r == codes.created:
            flash(_.reg.ok)
            raise web.redirect('/login/')
        else:
            flash(_.reg.fail)
            raise web.redirect('/reg/')

class User:
    def GET(self, id):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        return render.user(user=j)

class UserEdit:
    def GET(self, id):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        return render.user_edit(user=j)
    def POST(self, id):
        i = web.input()
        r, j = client.put('/users/%i/' % int(id))
        if r == codes.accepted:
            flash(_.user.edit.ok)
            raise web.redirect('/users/%i/' % int(id))
        else:
            flash(_.user.edit.fail)
            raise web.redirect('/users/%i/edit/' % int(id))


if __name__ == "__main__":
    app.run()