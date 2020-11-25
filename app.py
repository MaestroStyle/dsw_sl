import http.server
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import socketserver

class myHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        out = self.wfile
        url = self.path

        if url == "/":
            gmt = timezone("GMT")
            out.write(gmt.localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S %Z%z').encode("utf8"))
        elif url.count("/") == 1:
            loc_gmt = timezone("GMT").localize(datetime.now())

            name_tz = url[1:]
            tz = timezone(name_tz)
            # pytz.
            loc_dt = loc_gmt.astimezone(tz)

            out.write(loc_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z').encode("utf8"))
        else:
            out.write("You request is wrong!".encode("utf8"))

        # out.write(self.path.encode("utf8"))
        # out.write("\n".encode("utf8"))



        #
        # ip, port = self.client_address
        # client_address = f"You address is {ip}:{port}"
        # out.write(client_address.encode("utf8"))
        # out.write("\n".encode("utf8"))
        # out.write(f"You address is {self.address_string()}".encode("utf8"))

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=myHTTPRequestHandler)