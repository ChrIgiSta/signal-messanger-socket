#!/usr/bin/python

##
# Copyright (c) 2020, Staufi IoT - Frauenfeld Switzerland.
# All rights reserved.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
# @author: Christian Stauffer
# @date:   Apr 10 2020, Frauenfeld
# @file:   signal_socket.py
#
# @brief:  open a http server to send signal messages using signal-cli
#          available under git 'https://github.com/AsamK/signal-cli.git'
##

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import subprocess
import time
import urlparse
import simplejson


PORT_NUMBER = 16323
OWN_PHONE_NUMBER = '+10000000000'
SIGNAL_CLI = '/var/signal/build/install/signal-cli/bin/signal-cli'


class httpHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        try:
            self.send_response(204)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("No Content")
        except:
            self.send_response(500)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("Internal Server Error")

    def do_POST(self):
        try:
            urlPath = urlparse.urlparse(self.path)
            print("RX POST: " + str(urlPath.path))

            self.contentLength = self.rfile.read(int(self.headers['Content-Length']))
            jsonData = simplejson.loads(self.contentLength)
            print(jsonData['value1'])
            print(jsonData['value2'])

            if str(urlPath.path) == '/sms':
                process = subprocess.Popen([SIGNAL_CLI, '-u', str(OWN_PHONE_NUMBER), 'send', '-m', str(jsonData['value2']), str(jsonData['value1'])])

                self.send_response(200)
                self.end_headers()
                self.wfile.write("Signal message sent.")

            elif str(urlPath.path) == '/reg':
                process = subprocess.Popen([SIGNAL_CLI, '-u', str(OWN_PHONE_NUMBER), 'register'])

                self.send_response(200)
                self.end_headers()
                self.wfile.write("Number register.")

            elif str(urlPath.path) == '/verify':
                process = subprocess.Popen([SIGNAL_CLI, '-u', str(OWN_PHONE_NUMBER), 'verify', str(jsonData['value1'])])

                self.send_response(200)
                self.end_headers()
                self.wfile.write("Number verified.")

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write("unknown path")

        except:
            self.send_response(500)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("Internal Server Error")

try:
    httpServer = HTTPServer(('', PORT_NUMBER), httpHandler)
    print 'Http-Server started on port ' , PORT_NUMBER
    httpServer.serve_forever()

except KeyboardInterrupt:
    print 'shutting down...'
    server.socket.close()
