from django.contrib import admin
from karyawan.models import Pegawai

@admin.register(Pegawai)
class PegawaiAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'get_username', 'jabatan', 'divisi')
    search_fields = ('nama_lengkap', 'user__username', 'jabatan', 'divisi')
    list_filter = ('divisi', 'jabatan')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

