from django.db import models
from django.contrib.auth.models import User

class Pegawai(models.Model):
    """
    Model Profil Pegawai yang terhubung dengan Akun User Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pegawai')
    nama_lengkap = models.CharField(max_length=150, verbose_name="Nama Lengkap")
    jabatan = models.CharField(max_length=100, verbose_name="Jabatan")
    divisi = models.CharField(max_length=100, verbose_name="Divisi")

    class Meta:
        verbose_name = "Pegawai"
        verbose_name_plural = "Pegawai"

    def __str__(self):
        return f"{self.nama_lengkap} - {self.jabatan}"
