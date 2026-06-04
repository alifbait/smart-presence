from django.db import models
from karyawan.models import Pegawai

class Presensi(models.Model):
    """
    Model Transaksi Presensi Harian Pegawai.
    Satu pegawai hanya diperbolehkan memiliki satu rekaman presensi per tanggal.
    """
    STATUS_CHOICES = (
        ('Hadir', 'Hadir'),
        ('Terlambat', 'Terlambat'),
        ('Izin', 'Izin'),
        ('Alpa', 'Alpa'),
    )
    
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE, related_name='presensi', verbose_name="Pegawai")
    tanggal = models.DateField(verbose_name="Tanggal")
    jam_masuk = models.TimeField(null=True, blank=True, verbose_name="Jam Masuk")
    jam_pulang = models.TimeField(null=True, blank=True, verbose_name="Jam Pulang")
    status_kehadiran = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Hadir', verbose_name="Status Kehadiran")
    keterangan = models.TextField(null=True, blank=True, verbose_name="Keterangan")

    class Meta:
        verbose_name = "Presensi"
        verbose_name_plural = "Daftar Presensi"
        unique_together = ('pegawai', 'tanggal')

    def __str__(self):
        return f"{self.pegawai.nama_lengkap} - {self.tanggal} ({self.status_kehadiran})"


class PengajuanIzin(models.Model):
    """
    Model Transaksi Pengajuan Izin, Sakit, dan Cuti Pegawai.
    """
    JENIS_CHOICES = (
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Cuti', 'Cuti'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    )
    
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE, related_name='pengajuan_izin', verbose_name="Pegawai")
    jenis_izin = models.CharField(max_length=10, choices=JENIS_CHOICES, verbose_name="Jenis Izin")
    tanggal_mulai = models.DateField(verbose_name="Tanggal Mulai")
    tanggal_selesai = models.DateField(verbose_name="Tanggal Selesai")
    alasan = models.TextField(verbose_name="Alasan")
    bukti_file = models.FileField(upload_to='bukti_izin/', null=True, blank=True, verbose_name="Bukti File")
    status_persetujuan = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending', verbose_name="Status Persetujuan")
    catatan_admin = models.TextField(null=True, blank=True, verbose_name="Catatan Admin")
    dibuat_pada = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    diperbarui_pada = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    class Meta:
        verbose_name = "Pengajuan Izin"
        verbose_name_plural = "Daftar Pengajuan Izin"
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f"{self.pegawai.nama_lengkap} - {self.jenis_izin} ({self.tanggal_mulai} s/d {self.tanggal_selesai})"
