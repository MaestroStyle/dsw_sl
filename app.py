import http.server
import socketserver

class myHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        out = self.wfile
        out.write(self.path.encode("utf8"))
        out.write("\n".encode("utf8"))

        ip, port = self.client_address
        client_address = f"You address is {ip}:{port}"
        out.write(client_address.encode("utf8"))
        out.write("\n".encode("utf8"))
        out.write(f"You address is {self.address_string()}".encode("utf8"))

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=myHTTPRequestHandler)