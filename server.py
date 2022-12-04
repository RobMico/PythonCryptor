from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        temp = post_body.split(str.encode('='))
        if(temp[0]==str.encode('key')):
            print(f"IP:{self.client_address[0]};key:{temp[1]};")
            with open('keys.dat', "a") as f:
                f.write(f"IP:{self.client_address[0]};key:{temp[1]};\n")
        
            

        self.send_response(200)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=HttpGetHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()
run()