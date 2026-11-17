"""Web UI Manajemen Cuti Pegawai: python3 server.py  ->  http://localhost:8001"""
import json
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from cuti.controls import CariPengajuanCutiControl, CutiRepository, LihatRiwayatDanSisaCutiControl
from cuti.models import Pegawai, PengajuanCuti, SaldoCuti

crepo = CutiRepository()
andi, sari = Pegawai("1", "Andi", "Staf"), Pegawai("2", "Sari", "Analis")
crepo.pengajuan += [PengajuanCuti("P1", andi, date(2026, 12, 24), date(2026, 12, 31)),
                    PengajuanCuti("P2", sari, date(2026, 12, 28), date(2027, 1, 3)),
                    PengajuanCuti("P3", andi, date(2026, 3, 2), date(2026, 3, 4))]
crepo.saldo += [SaldoCuti(andi, 2026, 12, 11), SaldoCuti(sari, 2026, 12, 5)]


def j_cuti(p):
    return dict(id=p.id_pengajuan, nama=p.pegawai.nama, nip=p.pegawai.nip, mulai=str(p.tanggal_mulai),
                selesai=str(p.tanggal_selesai), lama=p.lama_cuti, jenis=p.jenis_cuti)


def api(path, q, body):
    g = lambda k, d=None: (q.get(k) or [d])[0]
    if path == "/api/cuti":
        bln, tgl = g("bulan"), g("tanggal")
        r = CariPengajuanCutiControl(crepo).cari(int(g("tahun", 2026)), int(bln) if bln else None, int(tgl) if tgl else None)
        return [j_cuti(p) for p in r]
    if path == "/api/cuti/riwayat":
        pg = next(p for p in (andi, sari) if p.nip == g("nip"))
        riwayat, sisa = LihatRiwayatDanSisaCutiControl(crepo).lihat(pg, int(g("tahun", 2026)))
        return dict(nama=pg.nama, riwayat=[j_cuti(p) for p in riwayat], sisa=sisa)
    raise KeyError(path)


class H(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json"):
        raw = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

    def _run(self, body):
        u = urlparse(self.path)
        try:
            self._send(200, api(u.path, parse_qs(u.query), body))
        except ValueError as e:
            self._send(400, {"error": str(e)})
        except KeyError:
            self._send(404, {"error": "tidak ditemukan"})

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self._run({})
        self._send(200, (Path(__file__).parent / "static" / "index.html").read_bytes(), "text/html")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self._run(json.loads(self.rfile.read(n) or b"{}"))

    def log_message(self, *a): pass


if __name__ == "__main__":
    print("Buka http://localhost:8001  (Ctrl+C untuk berhenti)")
    ThreadingHTTPServer(("127.0.0.1", 8001), H).serve_forever()
