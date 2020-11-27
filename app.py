import http.server
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
import pytz
import socketserver
import time

class myHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path

        if url[1:] in all_timezones:
            tz = timezone(url[1:])
            dt = datetime.now(tz)
        elif url == "/":
            gmt = timezone("GMT")
            dt = datetime.now(gmt)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"Unknow timezone: {url[1:]}".encode("utf8"))
            return
        self.send_response(200)
        self.end_headers()

        body_response = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        out_stream = self.wfile
        out_stream.write(body_response.encode("utf8"))

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=myHTTPRequestHandler)