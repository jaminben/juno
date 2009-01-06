import SocketServer
import BaseHTTPServer
import urlparse
import cgi

def serve(server):
    try:
        server.serve_forever()
    except:
        print 'interrupted; exiting juno...'
        server.socket.close()

class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self): self.do_request()
    def do_POST(self): self.do_request()
    def do_PUT(Self): self.do_request()
    def do_HEAD(self): self.do_request()
    def do_DELETE(self): self.do_request()
    
    def do_request(self):
        parsed = urlparse.urlparse(self.path)
        data_dict = {
             'REQUEST_URI': self.path, 
             'REQUEST_METHOD': self.command,
             'QUERY_STRING': parsed.query, 
             'DOCUMENT_URI': parsed.path if parsed.path[-1] == '/' else parsed.path + '/',
              }
        # TODO: Fix this, see TODO file      
        # perhaps: self.headers.getheader('content-type')
        data = str(self.headers).split('\r\n')
        for line in data:
            if not line: continue
            (x, y) = [a.strip() for a in line.split(':', 1)]
            data_dict[x] = y
        if self.command == 'POST':    
            data_dict['POST_DATA'] = self.rfile.read(int(data_dict['Content-Length']))
        self.wfile.write(self.process(parsed.path, self.command, **data_dict))

    def process(self, uri, method='*', **kwargs): return ''

def run_dev(addr, port, process_func):
    HTTPRequestHandler.process = process_func
    server = BaseHTTPServer.HTTPServer((addr, port), HTTPRequestHandler)
    print ''
    print 'running Juno development server, <C-c> to exit...'
    print 'connect to 127.0.0.1:%s to use your app...' %port
    print ''
    serve(server)

class SCGIRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        if data:
            request_dict = self.build_scgi_dict(data)
            uri = request_dict['DOCUMENT_URI']
            method = request_dict['REQUEST_METHOD']
            self.request.send(self.process(uri, method, **request_dict))
        self.request.close()

    def build_scgi_dict(self, data):
        """
        Might not be the best way to parse the SCGI request.  Doesn't use
        the provided length at all, so if for some reason a header starts
        with ',' then it will break (seems unlikely though).
        """
        data_len, data = data.split(':', 1)
        count = 0
        data_list = data.split(chr(0))
        data_dict = {}
        while data_list[count][0] != ',':
            data_dict[data_list[count]] = data_list[count + 1]
            count += 2
        msg = data_list[count][1:]
        data_dict['POST_DATA'] = msg
        return data_dict
    
    def process(self, uri, method='*', **kwargs): return ''

def run_scgi(addr, port, process_func):
    SCGIRequestHandler.process = process_func
    server = SocketServer.ThreadingTCPServer((addr, port), SCGIRequestHandler)
    print ''
    print 'running Juno SCGI server, <C-c> to exit...'
    print 'connect to 127.0.0.1:80 to use your app...'
    print ''
    serve(server)
