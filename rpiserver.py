
import os
import time
import datetime
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import subprocess


## Create HTTPServer to change date and time on rpi when rpi is not coonected to the internet
## Also allow to reboot or shutdown rpi when there is no keyboard
## Change ip addess to match
## Raspberry Pi W address and 
## select port
##
## Use a web browser and type: 
##     http://192.188.9.191:8008
## 

host_name = '192.168.8.191'
host_port = 8008


class MyHandler(BaseHTTPRequestHandler):


    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.protocol_version = 'HTTP/1.1'

        self.newdate = ""
        self.newtime = ""

        self.myTime = datetime.datetime.now()
        self.path = "/"


    def rpiShutdown (self):
        cmd = "sudo shutdown -h now"
        #cmd = "ls -la"
        pp=subprocess.Popen ( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        #print pp


    def rpiReboot (self):
        cmd = "sudo shutdown -r now"
        #cmd = "ls -la"
        pp=subprocess.Popen ( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        #print pp


    def setRpiDatetime (self, req):
        cmd = 'sudo date -s "%s"' % (req) 
        #cmd = "ls -la"
        pp=subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        #print pp


    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):

        myDateTime     = str(datetime.datetime.now())
        mydate, mytime = myDateTime.split()

        datestr = '''
            date (yyyy-mm-dd):    <input type="text"   name="dtdate"  value="%s"><br><br>
            time (hh:mm:ss.usec): <input type="text"   name="dttime"  value="%s"><br><br>
                                  <input type="submit" name="subdate" value="change"> Apply date time<br>
        ''' % (mydate, mytime)


        rpistr = '''
            rpi:   <input type="submit" name="rpishutdown" value="off"> sudo shutdown -h now<br><br>
            rpi:   <input type="submit" name="rpireboot"   value="reboot"> sudo shutdown -r now<br><br>
        '''

        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()


        html = '''
            <html>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <h1>RPI</h1>
            cpu %s
            <br>
            <form action="/" method="POST">
                <br>
                <br>
                <br>
                %s
                <br>
                <br>
                <br>
                %s
            </form>

            </body>
            </html>
        ''' % ( temp, datestr,rpistr)


        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))


    def do_POST(self):

        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        post_req  = post_data.split("&")
        #print post_req

        count = len (post_req)
        for ii in range (0,count):
            #print "request: ", post_req[ii] 
    
            if post_req[ii] == 'subdate=change':                 
                datetime = self.newdate + " " + self.newtime 
                #print "changing RPI datetime to:", datetime
                self.setRpiDatetime(datetime)

            elif post_req[ii] == 'rpishutdown=off': 
                self.rpiShutdown()

            elif post_req[ii] == 'rpireboot=reboot': 
                self.rpiReboot()
                
            else:

                if "dtdate=" in post_req[ii]:
                    self.newdate = post_req[ii].replace ("dtdate=","").replace("+"," ").replace("%3A", ":")
                    print "saving new date", self.newdate

                if "dttime=" in post_req[ii]:
                    self.newtime = post_req[ii].replace ("dttime=","").replace("+"," ").replace("%3A", ":")
                    print "saving new time", self.newtime

                pass
 

        self._redirect('/')    # Redirect back to the root url




def run ():

    server_address = (host_name, host_port)
    print("Server Starts - %s:%s" % (host_name, host_port))


    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()
  
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
        http_server.server_close()



while(True):
    try:
        run()
    except:
        time.sleep(30)



