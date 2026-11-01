"""Serve only a built artifact on loopback, retaining the old /docs/ preview URLs."""
from __future__ import annotations

import argparse
import functools
import http.server
import threading
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from build_publications import ROOT, build


def fingerprint(root):
    return tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size) for folder in ('content','docs','assets') for p in sorted((root/folder).rglob('*')) if p.is_file())


def serve(directory, port=8000, watch=False, preview_id=None):
    directory=Path(directory).resolve()
    build_root=(ROOT/'build').resolve()
    if not directory.is_relative_to(build_root):
        raise ValueError('Serve a generated artifact within build/, not the repository source')
    state={'fingerprint':fingerprint(ROOT)}
    lock=threading.Lock()
    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self,path):
            parts=urlsplit(path)
            mapped=parts.path[5:] if parts.path.startswith('/docs/') else parts.path
            return super().translate_path(urlunsplit(('', '', mapped, parts.query, parts.fragment)))

        def list_directory(self,path):
            self.send_error(404,'Page not found')

        def end_headers(self):
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Cache-Control','no-cache')
            if preview_id:
                self.send_header('X-Robots-Tag','noindex, nofollow')
            super().end_headers()

        def do_GET(self):
            if watch:
                with lock:
                    changed=fingerprint(ROOT)
                    if changed != state['fingerprint']:
                        try:
                            build(output=directory,preview_id=preview_id)
                            state['fingerprint']=changed
                            print('Rebuilt publications from changed content.',flush=True)
                        except Exception as error:
                            print(f'Build failed: {error}',flush=True)
                            self.send_error(503,'Content validation failed; check the server log')
                            return
            super().do_GET()
    handler=functools.partial(Handler,directory=str(directory))
    with http.server.ThreadingHTTPServer(('127.0.0.1',port),handler) as server:
        print(f'Local publications: http://localhost:{server.server_port}/publications/',flush=True)
        if preview_id:
            print('Private preview build. Do not deploy this directory.',flush=True)
        server.serve_forever()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8000)
    parser.add_argument('--watch',action='store_true')
    args=parser.parse_args()
    build()
    serve(ROOT/'build/site',args.port,args.watch)
