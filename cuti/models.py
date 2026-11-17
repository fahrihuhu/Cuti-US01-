"""Domain model US-01 Manajemen Cuti Pegawai."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class HRDManajer:
    id_hrd: str
    nama: str
    email: str


@dataclass
class Pegawai:
    nip: str
    nama: str
    jabatan: str
    email: str = ""


@dataclass
class PengajuanCuti:
    id_pengajuan: str
    pegawai: Pegawai
    tanggal_mulai: date
    tanggal_selesai: date
    jenis_cuti: str = "Tahunan"
    status: str = "Diajukan"

    @property
    def lama_cuti(self) -> int:
        """Atribut turunan /lamaCuti (hari kalender, inklusif)."""
        return (self.tanggal_selesai - self.tanggal_mulai).days + 1


@dataclass
class SaldoCuti:
    pegawai: Pegawai
    tahun: int
    jatah_cuti: int
    cuti_terpakai: int = 0

    @property
    def sisa_cuti(self) -> int:
        """Atribut turunan /sisaCuti = jatah - terpakai."""
        return self.jatah_cuti - self.cuti_terpakai
