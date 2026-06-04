from karyawan.decorators import get_user_role

def role_context(request):
    """
    Context processor untuk mengekspos role user yang sedang login ke seluruh template HTML.
    """
    if request.user.is_authenticated:
        role = get_user_role(request.user)
        return {
            'user_role': role,
            'is_superuser_role': role == 'superuser',
            'is_admin_role': role == 'admin',
            'is_pegawai_role': role == 'pegawai',
        }
    return {
        'user_role': None,
        'is_superuser_role': False,
        'is_admin_role': False,
        'is_pegawai_role': False,
    }
