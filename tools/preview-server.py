#!/usr/bin/env python3
"""Lokaler Preview-Server für Lighthouse-Messungen.

Der mitgelieferte `python3 -m http.server` antwortet ohne Keep-Alive und ohne
Kompression. Jede Anfrage kostet damit einen neuen TCP-Handshake, was
gemessene Ladezeiten schlechter aussehen lässt als sie sind – GitHub Pages
liefert HTTP/1.1 mit Keep-Alive, gzip und Cache-Header.

Aufruf:  python3 tools/preview-server.py [verzeichnis] [port]
"""

import gzip
import mimetypes
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

GZIP_AB = 1024  # darunter lohnt sich der Aufwand nicht
KOMPRESSION = {"text/html", "text/css", "application/javascript", "image/svg+xml",
               "application/json", "text/plain"}


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _datei(self):
        """Pfad der angeforderten Datei (Ordner -> index.html) oder None."""
        pfad = os.path.join(self.directory, self.path.lstrip("/").split("?")[0])
        if os.path.isdir(pfad):
            pfad = os.path.join(pfad, "index.html")
        return pfad if os.path.isfile(pfad) else None

    def _komprimiert(self):
        """Liefert gzip-Payload oder None, wenn nicht zu komprimieren."""
        pfad = self._datei()
        if not pfad:
            return None
        typ, _ = mimetypes.guess_type(pfad)
        if typ not in KOMPRESSION:
            return None
        with open(pfad, "rb") as f:
            roh = f.read()
        return gzip.compress(roh, 6) if len(roh) >= GZIP_AB else None

    def end_headers(self):
        # GitHub Pages liefert max-age=600 für statische Dateien – Nachahmung
        self.send_header("Cache-Control", "max-age=600")
        super().end_headers()

    def _antwort(self, daten=None):
        """200 mit (optional) gzip-Body bzw. HEAD-Köpfen."""
        typ, _ = mimetypes.guess_type(self._datei() or self.path)
        self.send_response(200)
        self.send_header("Content-Type", typ or "application/octet-stream")
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Vary", "Accept-Encoding")
        self.send_header("Content-Length", str(len(daten)))
        self.end_headers()
        if daten:
            self.wfile.write(daten)

    def do_GET(self):
        daten = self._komprimiert()
        if daten is None:
            return super().do_GET()
        self._antwort(daten)

    def do_HEAD(self):
        daten = self._komprimiert()
        if daten is None:
            return super().do_HEAD()
        self._antwort(daten)

    def log_message(self, *a):  # still
        pass


if __name__ == "__main__":
    verzeichnis = sys.argv[1] if len(sys.argv) > 1 else "public"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1314
    handler = partial(Handler, directory=verzeichnis)
    print(f"Serve {verzeichnis} auf http://127.0.0.1:{port}/ (Keep-Alive + gzip)")
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
