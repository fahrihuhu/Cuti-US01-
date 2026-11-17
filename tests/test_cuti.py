import unittest
from datetime import date

from cuti.controls import CariPengajuanCutiControl, CutiRepository, LihatRiwayatDanSisaCutiControl, periode
from cuti.models import Pegawai, PengajuanCuti, SaldoCuti


class TestCuti(unittest.TestCase):
    def setUp(self):
        self.a, self.b = Pegawai("1", "Andi", "Staf"), Pegawai("2", "Sari", "Analis")
        self.repo = CutiRepository()
        self.repo.pengajuan += [
            PengajuanCuti("P1", self.a, date(2026, 12, 24), date(2026, 12, 31)),
            PengajuanCuti("P2", self.b, date(2026, 12, 28), date(2027, 1, 3)),
            PengajuanCuti("P3", self.a, date(2026, 3, 2), date(2026, 3, 4)),
        ]
        self.repo.saldo.append(SaldoCuti(self.a, 2026, 12, 11))

    def test_lama_cuti_inklusif(self):
        self.assertEqual(self.repo.pengajuan[0].lama_cuti, 8)

    def test_periode_tahun_bulan_tanggal(self):
        self.assertEqual(periode(2026), (date(2026, 1, 1), date(2026, 12, 31)))
        self.assertEqual(periode(2026, 2), (date(2026, 2, 1), date(2026, 2, 28)))
        self.assertEqual(periode(2026, 2, 5), (date(2026, 2, 5), date(2026, 2, 5)))
        with self.assertRaises(ValueError):
            periode(2026, None, 5)

    def test_cari_per_bulan_dan_irisan(self):
        c = CariPengajuanCutiControl(self.repo)
        self.assertEqual([p.id_pengajuan for p in c.cari(2026, 12)], ["P1", "P2"])
        self.assertEqual([p.id_pengajuan for p in c.cari(2027, 1, 2)], ["P2"])
        self.assertEqual(len(c.cari(2026)), 3)

    def test_tidak_ada_pengajuan(self):
        self.assertEqual(CariPengajuanCutiControl(self.repo).cari(2026, 7), [])

    def test_riwayat_dan_sisa_cuti(self):
        riwayat, sisa = LihatRiwayatDanSisaCutiControl(self.repo).lihat(self.a, 2026)
        self.assertEqual([p.id_pengajuan for p in riwayat], ["P3", "P1"])
        self.assertEqual(sisa, 1)
        self.assertIsNone(LihatRiwayatDanSisaCutiControl(self.repo).lihat(self.b, 2026)[1])


if __name__ == "__main__":
    unittest.main()
