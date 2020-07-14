import tornado.template
import tornado.ioloop
import tornado.web
import os, pwd, grp

TEMPLATE = '''
<html>
 <head><title> 🐱‍👤Hello Hacker</title></head>
 <body style="background: #00FFFF">
 <h1 style="text-align:center; font-size:5rem;"> 🐱‍👤 The Usual Suspects 🐱‍👤 </h1>
 <br />
 <h2 style="text-align:center; font-size:4rem;"> You Have Arrived FOO ! </h2>
 <br />
 <p style="text-align:center; font-size:2rem;"> 
 It's so good to see you here. I am your webpage. 
 I think you don't know what I actually look like :) <br/>
 </p>
 <br/> <br/>
 <p style="text-align:center; font-size:2rem;">
 Oh I heard you're looking for my secret. Here's a little hint: <br/>
 My favourite Ice Cream flavour is <strong>Cookies&Cream</strong>
 </p>
 </body>
</html>
'''
#hello= open("hello.txt").read()
class MainHandler(tornado.web.RequestHandler):
 
    def get(self):
        person= {'name':"", 'secret':"csictf{my_secret_is_not_out}"}
        #if self.get_argument('name')==True:
        person['name']= self.get_argument('name','')
        template_data = TEMPLATE.replace("FOO",person['name'])
        t = tornado.template.Template(template_data)
        self.set_secure_cookie("mycookie", "myvalue")
        self.write(t.generate(person=person,application=application))
        
        if self.get_secure_cookie("mycookie")==b"youwin":
            self.write(open("rf.txt").read())
        else:
            self.write("Better luck next time!")
        cookie=self.get_secure_cookie("mycookie")
        print(cookie)
        



application = tornado.web.Application([
    (r"/test", MainHandler)
    
], debug=True, static_path=None, template_path=None, cookie_secret=open("cs.txt").read()
 
if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

def drop_privileges(uid_name='nobody', gid_name='nogroup'):
    if os.getuid() != 0:
        return

    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    os.setgroups([])
 
    os.setgid(running_gid)
    os.setuid(running_uid)

    old_umask = os.umask(077)
