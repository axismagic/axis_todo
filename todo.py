import web
import model

urls = (
    '/', 'Index',
    '/developer_done/(\d+)', 'developer_done',
    '/qa_done/(\d+)', 'qa_done',
    '/delete/(\d+)', 'delete'
)

render = web.template.render('templates', base='base')

def getUserbyIP():
    return model.getUserbyIP(web.ctx.ip)

class Index:
        
    def GET(self):
        user = getUserbyIP()
        isqa = model.is_qa(user)
        todos = model.get_todos()
        return render.index(todos, user, isqa)

    def POST(self):
        user = getUserbyIP()
        model.new_todo(web.webapi.input().title,user)
        raise web.seeother('/')

class developer_done:

    def POST(self, id):
        id = int(id)
        status = 1
        if ('status' in web.webapi.input()):
            status = 0
        model.developer_done_todo(id,status)
        raise web.seeother('/')

class qa_done:

    def POST(self, id):
        id = int(id)
        status = 1
        if ('status' in web.webapi.input()):
            status = 0
        model.qa_done_todo(id,status)
        raise web.seeother('/')

class delete:

    def POST(self, id):
        id = int(id)
        model.delete(id)
        raise web.seeother('/')

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()