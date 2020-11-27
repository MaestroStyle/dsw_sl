import http.server
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
import json
import pytz
import socketserver
import time

class myHTTPRequestHandler(http.server.CGIHTTPRequestHandler):
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
            self.wfile.write(f"Unknown timezone: {url[1:]}".encode("utf8"))
            return
        self.send_response(200)
        self.end_headers()

        body_response = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        self.wfile.write(body_response.encode("utf8"))

    def do_POST(self):
        url = self.path

        if url[1:] == "api/v1/convert":
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            data = json.loads(post_body)

            tz = timezone(data["tz"])
            dt = tz.localize(datetime.strptime(data["date"], "%m.%d.%Y %H:%M:%S"))
            target_tz = timezone(data["target_tz"])
            convert_dt = dt.astimezone(target_tz)

            self.send_response(200)
            self.end_headers()

            body_response = convert_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            self.wfile.write(body_response.encode("utf8"))

        elif url[1:] == "api/v1/datediff":
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            data = json.loads(post_body)

            first_tz = timezone(data["first_tz"])
            first_dt = first_tz.localize(datetime.strptime(data["first_date"], "%m.%d.%Y %H:%M:%S"))
            second_tz = timezone(data["second_tz"])
            second_dt = second_tz.localize(datetime.strptime(data["second_date"], "%m.%d.%Y %H:%M:%S"))
            time_delta = first_dt - second_dt
            self.send_response(200)
            self.end_headers()

            body_response = f"{time_delta.seconds}"
            self.wfile.write(body_response.encode("utf8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"Wrong url: {url[1:]}".encode("utf8"))
        # self.wfile.write(url.encode("utf8"))


def run(server_class=http.server.HTTPServer, handler_class=http.server.CGIHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=myHTTPRequestHandler)