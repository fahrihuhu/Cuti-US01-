"""Control US-01: UC-01/UC-02 Cari Pengajuan Cuti, UC-03 Lihat Riwayat & Sisa Cuti."""
from __future__ import annotations

import calendar
from datetime import date
from typing import List, Optional, Tuple

from .models import Pegawai, PengajuanCuti, SaldoCuti


class CutiRepository:
    def __init__(self) -> None:
        self.pengajuan: List[PengajuanCuti] = []
        self.saldo: List[SaldoCuti] = []


def periode(tahun: int, bulan: Optional[int] = None, tanggal: Optional[int] = None) -> Tuple[date, date]:
    """UC-01 Pilih Periode Cuti: tahun wajib, bulan dan tanggal opsional."""
    if tanggal is not None and bulan is None:
        raise ValueError("bulan wajib diisi bila tanggal dipilih")
    if bulan is None:
        return date(tahun, 1, 1), date(tahun, 12, 31)
    if tanggal is None:
        return date(tahun, bulan, 1), date(tahun, bulan, calendar.monthrange(tahun, bulan)[1])
    return date(tahun, bulan, tanggal), date(tahun, bulan, tanggal)


class CariPengajuanCutiControl:
    """UC-02: pengajuan yang periodenya beririsan dengan periode terpilih."""

    def __init__(self, repo: CutiRepository) -> None:
        self._repo = repo

    def cari(self, tahun: int, bulan: Optional[int] = None, tanggal: Optional[int] = None) -> List[PengajuanCuti]:
        awal, akhir = periode(tahun, bulan, tanggal)
        hasil = [p for p in self._repo.pengajuan if p.tanggal_mulai <= akhir and p.tanggal_selesai >= awal]
        return sorted(hasil, key=lambda p: (p.tanggal_mulai, p.pegawai.nama))


class LihatRiwayatDanSisaCutiControl:
    """UC-03: riwayat cuti dan sisa cuti pegawai pada tahun berjalan."""

    def __init__(self, repo: CutiRepository) -> None:
        self._repo = repo

    def lihat(self, pegawai: Pegawai, tahun: int) -> Tuple[List[PengajuanCuti], Optional[int]]:
        riwayat = sorted((p for p in self._repo.pengajuan if p.pegawai.nip == pegawai.nip),
                         key=lambda p: p.tanggal_mulai)
        saldo = next((s for s in self._repo.saldo if s.pegawai.nip == pegawai.nip and s.tahun == tahun), None)
        return riwayat, (saldo.sisa_cuti if saldo else None)
