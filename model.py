import web

db = web.database(dbn='sqlite', db='todo')

'''
CREATE TABLE todo (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user TEXT,
    developerstatus INTEGER,
    qastatus INTEGER
);
'''
def get_todos():
    return db.select('todo', order='user') #, order='qastatus desc, developerstatus desc'

def new_todo(text,user):
    db.insert('todo', title=text, user=user, developerstatus=1,qastatus=1)

def developer_done_todo(id,status):
    db.update('todo', where="id=$id", vars=locals(), developerstatus=status)
	
def qa_done_todo(id,status):
    db.update('todo', where="id=$id", vars=locals(), qastatus=status)
	
def delete(id):
    db.delete('todo', where="id=$id", vars=locals())
	

'''
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name TEXT,
    membertype INTEGER,/*1:dev,2:qa,3:po*/
    ip TEXT,
    host TEXT
);
'''
def is_qa(user):
    return len(db.select('user',where="name=$user and membertype=2", vars=locals()).list()) > 0

def getUserbyIP(ip):
    result = db.select('user',where="ip=$ip", vars=locals()).list()
    if len(result) == 0:
        return ""
    else:
        return result[0].name
    
def update_userip_byhostname():
    import socket
    users =  db.select('user').list()
    for user in users:    
        ip = socket.gethostbyname(user.host)
        db.update('user', where="id=$user.id", vars=locals(), ip=ip)
        
if __name__ == '__main__':
    update_userip_byhostname();
