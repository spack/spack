import argparse
import http.server
import os
import subprocess


PORT = os.environ.get("SPACK_MAPPING_SERVER_PORT", 23456)
URL = os.environ.get("SPACK_MAPPING_SERVER_URL", "localhost")

counter = 0

REST_ROOT = os.path.dirname(os.path.realpath(__file__))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        script = REST_ROOT + self.path + ".py"

        if not os.path.exists(script):
            self.send_response(501)
            self.send_header("Content-type", "text/http")
            self.end_headers()
            self.wfile.write(f"Unknown Path: {script}".encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()

        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n).decode("utf-8")
        out = b"[]"
        err = b"null"
        if data:
            proc = subprocess.run([script, data], capture_output=True)
            out, err = proc.stdout, proc.stderr
            if not out:
                out = b"{}"

        global counter
        counter += 1
        if False:
            message = f"""
            {{
              "out": {out.decode()},
              "err": "{err.decode()}"
            }}
            """

            self.wfile.write(message.encode("utf-8"))
        else:
            if err:
                print(err.decode())
            self.wfile.write(out)


def start_service():
    httpd = http.server.HTTPServer((URL, PORT), Handler)
    print("Server address: ", httpd.server_address)
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=REST_ROOT)
    parser.add_argument("--url", default=URL)
    parser.add_argument("--port", default=PORT)

    args = parser.parse_args()

    REST_ROOT = args.root
    URL = args.url
    PORT = args.port

    start_service()
