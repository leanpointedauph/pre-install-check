"""pre-install-check service. Stdlib only."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import checker
import paywall

PRICE = 0.02
SITE = "https://leanpointedauph-site-production.up.railway.app/products"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj, extra=None):
        if isinstance(obj, dict):
            obj.setdefault("ai_disclosure", checker.AI_DISCLOSURE)
        data = obj.encode() if isinstance(obj, str) else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send(200, {"service": "pre-install-check",
                             "endpoint": "POST /check",
                             "body": {"packages": [{"name": "x", "ecosystem": "pypi|npm"}]},
                             "max_packages": checker.MAX_PACKAGES,
                             "price_usd": PRICE, "payment": "USDC on Base, X-Payment-Tx header",
                             "products": SITE})
        elif self.path == "/stats":
            s = paywall.stats_json()
            self._send(200, s if isinstance(s, (dict, str)) else json.loads(s))
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/check":
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = -1
        if n < 0 or n > 65536:
            return self._send(400, {"error": "bad body size"})
        pkgs, err = checker.parse_request(self.rfile.read(n))
        if err:  # validate before charging: bad input is never billed
            return self._send(400, {"error": err})
        ok, code, body = paywall.check(dict(self.headers), PRICE, "pre-install check")
        if not ok:
            return self._send(code, body)
        self._send(200, checker.check_all(pkgs))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
