from django import forms
from presensi.models import Presensi, PengajuanIzin

class PresensiForm(forms.ModelForm):
    """
    Form untuk mencatat keterangan tambahan ketika presensi.
    """
    class Meta:
        model = Presensi
        fields = ['keterangan']
        widgets = {
            'keterangan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan catatan tambahan jika diperlukan (misalnya: urusan dinas luar, keterlambatan macet, dll.)',
                'rows': 3
            })
        }


class PengajuanIzinForm(forms.ModelForm):
    """
    Formulir untuk mengajukan Izin, Sakit, atau Cuti.
    """
    class Meta:
        model = PengajuanIzin
        fields = ['jenis_izin', 'tanggal_mulai', 'tanggal_selesai', 'alasan', 'bukti_file']
        widgets = {
            'jenis_izin': forms.Select(attrs={'class': 'form-select'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'alasan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tuliskan alasan pengajuan secara lengkap dan jelas...',
                'rows': 4
            }),
            'bukti_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
