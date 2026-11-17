"""Demo US-01: python3 demo.py"""
from datetime import date

from cuti.controls import CariPengajuanCutiControl, CutiRepository, LihatRiwayatDanSisaCutiControl
from cuti.models import Pegawai, PengajuanCuti, SaldoCuti

print("=== US-01: pengajuan cuti Desember 2026 ===")
repo = CutiRepository()
a1, a2 = Pegawai("1", "Andi", "Staf"), Pegawai("2", "Sari", "Analis")
repo.pengajuan += [PengajuanCuti("P1", a1, date(2026, 12, 24), date(2026, 12, 31)), PengajuanCuti("P2", a2, date(2026, 12, 28), date(2027, 1, 3))]
repo.saldo.append(SaldoCuti(a1, 2026, 12, 3))
for p in CariPengajuanCutiControl(repo).cari(2026, 12):
    print(f"{p.pegawai.nama}: {p.tanggal_mulai} s.d. {p.tanggal_selesai} ({p.lama_cuti} hari)")
riwayat, sisa = LihatRiwayatDanSisaCutiControl(repo).lihat(a1, 2026)
print("Andi: riwayat", len(riwayat), "pengajuan, sisa cuti", sisa)
