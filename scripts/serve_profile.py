#!/usr/bin/env python3
"""Serve trust.mobileconfig over the LAN so the iPad can install it.

GitHub Pages serves .mobileconfig as application/octet-stream, which iOS 9
refuses; the only way to get the right Content-Type is to serve it ourselves.
Plain HTTP is enough here and avoids a chicken-and-egg problem: the profile
exists to add the roots that HTTPS would need.

    python3 scripts/serve_profile.py            # port 8123
    python3 scripts/serve_profile.py 9000       # other port
"""
import http.server
import os
import socket
import socketserver
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = os.path.join(ROOT, "trust.mobileconfig")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123

PAGE = """<!doctype html>
<html lang="hr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalacija profila</title></head>
<body style="margin:0;background:#000;color:#e8eef7;
             font:20px/1.5 -apple-system,Helvetica,Arial,sans-serif;padding:40px">
<h1 style="font-size:28px;margin:0 0 8px">Weather Hub &mdash; trust store</h1>
<p style="color:#9a9a9a;margin:0 0 28px">Dodaje Let's Encrypt i Google Trust
Services korijene koje iOS 9 nema.</p>
<a href="/trust.mobileconfig"
   style="display:block;text-align:center;background:#1c1c1c;color:#fff;
          text-decoration:none;padding:26px;border-radius:12px;font-size:24px;
          border:1px solid #4a4a4a">Instaliraj profil</a>
<p style="color:#666;font-size:16px;margin-top:26px">
Nakon instalacije: Postavke &rarr; Op&cacute;enito &rarr; Profili mora pokazati
<i>Weather Hub trust store</i>.</p>
</body></html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path.split("?")[0] == "/trust.mobileconfig":
            try:
                with open(PROFILE, "rb") as handle:
                    body = handle.read()
            except OSError:
                self.send_error(404, "trust.mobileconfig not found")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/x-apple-aspen-config")
            self.send_header("Content-Disposition", 'attachment; filename="trust.mobileconfig"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def local_addresses():
    addresses = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            addresses.add(info[4][0])
    except OSError:
        pass
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(("192.168.1.1", 80))
        addresses.add(probe.getsockname()[0])
        probe.close()
    except OSError:
        pass
    return sorted(a for a in addresses if not a.startswith("127."))


def main():
    if not os.path.exists(PROFILE):
        print("missing:", PROFILE)
        return 1
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as server:
        print("profile: %s (%d bytes)" % (PROFILE, os.path.getsize(PROFILE)))
        for address in local_addresses() or ["<your-lan-ip>"]:
            print("open on the iPad:  http://%s:%d" % (address, PORT))
        print("ctrl-c to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
