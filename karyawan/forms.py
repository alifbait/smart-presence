from django import forms
from django.contrib.auth.models import User
from karyawan.models import Pegawai

class PegawaiForm(forms.ModelForm):
    """
    Form terpadu untuk pendaftaran dan pengubahan data Pegawai serta Akun User.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username login'})
    )
    password = forms.CharField(
        required=False,
        label="Kata Sandi (Password)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kata sandi rahasia'})
    )
    role = forms.ChoiceField(
        choices=Pegawai.ROLE_CHOICES,
        required=True,
        label="Role / Peran",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Pegawai
        fields = ['nama_lengkap', 'jabatan', 'divisi', 'role']
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap pegawai'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Staff IT, Supervisor'}),
            'divisi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Teknologi Informasi, HRD'}),
        }

    def __init__(self, *args, **kwargs):
        # Mengeluarkan parameter tambahan 'is_edit' untuk membedakan mode tambah/edit
        self.is_edit = kwargs.pop('is_edit', False)
        super(PegawaiForm, self).__init__(*args, **kwargs)
        
        # Jika sedang mengedit pegawai yang sudah ada
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['role'].initial = self.instance.role
            self.fields['password'].required = False
            self.fields['password'].help_text = "Kosongkan jika Anda tidak ingin mengganti kata sandi."
        else:
            # Kata sandi wajib diisi jika menambah pegawai baru
            self.fields['password'].required = True
            self.fields['role'].initial = 'pegawai'

    def clean_username(self):
        """
        Validasi untuk memastikan keunikan username di database.
        """
        username = self.cleaned_data.get('username')
        user_query = User.objects.filter(username=username)
        
        # Jika mengedit, kecualikan akun user pegawai yang bersangkutan
        if self.is_edit and self.instance.pk:
            user_query = user_query.exclude(pk=self.instance.user.pk)
            
        if user_query.exists():
            raise forms.ValidationError("Nama pengguna (username) ini sudah digunakan. Silakan pilih yang lain.")
        return username
