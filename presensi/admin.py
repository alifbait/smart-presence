from django.contrib import admin
from presensi.models import Presensi

@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    """
    Konfigurasi Model Presensi pada Django Admin Panel.
    """
    list_display = ('pegawai', 'tanggal', 'jam_masuk', 'jam_pulang', 'status_kehadiran')
    search_fields = ('pegawai__nama_lengkap', 'tanggal', 'status_kehadiran')
    list_filter = ('status_kehadiran', 'tanggal')
    ordering = ('-tanggal', '-jam_masuk')
