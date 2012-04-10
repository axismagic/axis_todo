import web
import model

urls = (
    '/', 'Index',
    '/developer_done/(\d+)', 'developer_done',
    '/qa_done/(\d+)', 'qa_done',
    '/delete/(\d+)', 'delete',
    '/backup/(\d+)','backup'
)

render = web.template.render('templates', base='base')

def getUserbyIP():
    return model.getUserbyIP(web.ctx.ip)

class Index:
    def GET(self):
        debug = int(web.webapi.input(debug=0).debug)
        user = getUserbyIP()
        isqa = model.is_qa(user)
        todos = model.get_todos(debug)
        return render.index(todos, user, isqa, debug)

    def POST(self):
        user = getUserbyIP()
        title = web.webapi.input().title;
        model.new_todo(title,user)
        raise web.seeother(web.ctx.env.get('HTTP_REFERER','/'))

class developer_done:
    def POST(self, id):
        id = int(id)
        status = 1
        if ('status' in web.webapi.input()):
            status = 0
        model.developer_done_todo(id,status)
        raise web.seeother(web.ctx.env.get('HTTP_REFERER','/'))

class qa_done:
    def POST(self, id):
        id = int(id)
        status = 1
        if ('status' in web.webapi.input()):
            status = 0
        model.qa_done_todo(id,status)
        raise web.seeother(web.ctx.env.get('HTTP_REFERER','/'))

class delete:
    def POST(self, id):
        id = int(id)
        model.delete(id)
        raise web.seeother(web.ctx.env.get('HTTP_REFERER','/'))
    
class backup:
    def GET(self, id):
        id = int(id)
        model.sprint_backup(id)
        raise web.seeother(web.ctx.env.get('HTTP_REFERER','/'))

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()