#  coding: utf-8 
import socketserver,os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_receive = self.data.decode('utf-8')
        request_commd = data_receive.split('\r\n')[0]
        command = request_commd.split(' ')[0]
        Request_URL = request_commd.split(' ')[1]
        
        path = ""
        if command == "GET":
            if "css" not in Request_URL:
                if "index.html" not in Request_URL:
                    if Request_URL[-1] == "/":
                        Request_URL = Request_URL + "index.html"
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:"+ Request_URL + "/" + "\r\n\r\n301 Moved Permanently",'utf-8'))
                        return
            path = "./www" + Request_URL
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed",'utf-8'))
            return
        if ".html" in Request_URL:
            self.webSever_handle(path,"text/html")
        elif ".css" in Request_URL:
            self.webSever_handle(path,"text/css")
        self.request.sendall(bytearray("OK",'utf-8'))

    def webSever_handle(self,path,type):
        if os.path.exists(path):
            file = open(path,"r")
            data = file.read()
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" + type + "\r\n"+"\r\n\r\n"+data,'utf-8'))
            return
        else:
            self.request.sendall(bytearray('HTTP/1.1 404 Not Found\r\n\r\n404 Not Found','utf-8'))
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
