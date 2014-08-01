from __future__ import with_statement
import SimpleHTTPServer
import SocketServer
import os
import posixpath
import urllib
import urlparse
import webbrowser


def ui_hook(arg, args, pipeline):
    return args, pipeline.before("store", ui=lambda d: dict(d, **read(d)))


hooks = {
    "--long": ui_hook,
    "-l": ui_hook
}


class MyHttpServer(SocketServer.TCPServer):
    def serve_until_data_received(self, data):
        self.input_data = data
        self.output_data = None
        while not self.output_data:
            self.handle_request()

        return {k: v[0] for k, v in urlparse.parse_qs(self.output_data).items()}


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        static_path = os.path.dirname(__file__) + "/static/"

        def translate_path(self, path):
            """Translate a /-separated PATH to the local filename syntax.

            Components that mean special things to the local file system
            (e.g. drive or directory names) are ignored.  (XXX They should
            probably be diagnosed.)

            """
            # abandon query parameters
            path = urlparse.urlparse(path)[2]
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = MyRequestHandler.static_path
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)

            print path
            return path

        # TODO: Index should contain the body passed from command line.
        # TODO: External CSS/JS files should be packaged within app, for offline access
        # def render_index(self):
        #     f = self.send_head()
        #     if f:
        #         self.copyfile(f, self.wfile)
        #         f.close()
        #
        # def do_GET(self):
        #     print "*" * 100
        #     print self.path
        #     print "*" * 100
        #     if self.path == '/':
        #         return self.render_index()
        #     else:
        #         return super(MyRequestHandler, self).do_GET()

        def do_POST(self):
            length = int(self.headers.getheader('content-length'))
            self.server.output_data = self.rfile.read(length)
            self.send_response(201)
            self.end_headers()
            with open(MyRequestHandler.static_path + "done.html") as f:
                self.copyfile(f, self.wfile)

            self.finish()


def read(data):
    server = MyHttpServer(('127.0.0.1', 0), MyRequestHandler)
    port = server.server_address[1]
    webbrowser.open("http://127.0.0.1:%s" % port)
    return server.serve_until_data_received(data)