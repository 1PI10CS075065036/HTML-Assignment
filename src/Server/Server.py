'''
Created on 23-Mar-2013

@author: Sai Gopal
'''
import shutil
from SDK import SDK
from os import sep ,remove
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class HandleReq(BaseHTTPRequestHandler):
    def do_GET(self):
        curdir='..//RES'
        try:
            if self.path.endswith("gps.html"):
                
                userag=self.headers['User-Agent']
                if SDK.getOS(userag) != None:
                    
                    x=SDK.getDisplayHeight(userag)
                    if x != None:
                        x=str(int(x))
                    else :
                        x=400
                    y=SDK.getDisplayWidth(userag)
                    if y != None:
                        y=str(int(x))
                    else :
                        y=300
                    
                    
                    
                    f = open(curdir + self.path) 
                    shutil.copy2(curdir + self.path,'tempgps.html')
                    f.close()
                    w=open('temp-resgps.html','w')
                    for line in open('tempgps.html'):
                        if line.find('size') > -1:
                            w.write(line.replace('XXXxYYY',x+'x'+y))
                        else:
                            w.write(line)
                    f.close()
                    w.close()
                    remove('tempgps.html')    
                    f=open("temp-resgps.html")
                    self.send_response(200)
                    self.send_header('Content-type',    'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    remove('temp-resgps.html')
                    return     
                else:
                    f = open(curdir + '\\notamob.html') 
                    self.send_response(200)
                    self.send_header('Content-type',    'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return     
            
            if self.path.endswith("cam.html"):
                
                userag=self.headers['User-Agent']
              
                if SDK.getOS(userag) != None:
                    
                    if SDK.isSecCam(userag) == True:
                        x=SDK.getDisplayHeight(userag)
                        if x != None:
                            x=str(int(x)/2)
                        else :
                            x=400
                        y=SDK.getDisplayWidth(userag)
                        if y != None:
                            y=str(int(x))
                        else :
                            y=300
                        
                        
                        
                        f = open(curdir + self.path) 
                        shutil.copy2(curdir + self.path,'tempcam.html')
                        f.close()
                        w=open('temp-rescam.html','w')
                        for line in open('tempcam.html'):
                            if line.find('width') > -1:
                                w.write(line.replace('width="YYY" height="XXX"','width="'+y+'" height="'+x+'"'))
                            elif line.find('YYY,XXX') > -1:    
                                w.write(line.replace('YYY,XXX',y+','+x))
                            else:
                                w.write(line)
                        f.close()
                        w.close()
                        remove('tempcam.html')    
                        f=open("temp-rescam.html")
                        self.send_response(200)
                        self.send_header('Content-type',    'text/html')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                        remove('temp-rescam.html')
                        return     
                    else:
                        f = open(curdir + '\\notasecmob.html') 
                        self.send_response(200)
                        self.send_header('Content-type',    'text/html')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                        return
                else:
                    f = open(curdir + '\\notamob.html') 
                    self.send_response(200)
                    self.send_header('Content-type',    'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return
            else:
                f = open(curdir + sep + 'index.html')
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return   
            
              
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        
if __name__ == '__main__':
    try:
        server = HTTPServer(('', 80), HandleReq)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()