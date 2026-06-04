# Inisialisasi modul Django utama.
# Bagian ini ditambahkan untuk mendukung PyMySQL sebagai alternatif driver MySQL.
# Sangat membantu jika 'mysqlclient' mengalami kendala instalasi pada Windows.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


# Monkeypatch: Perbaikan kompatibilitas Django 5.0 dengan Python 3.14
# Python 3.14 melarang pengaturan atribut pada objek super() proxy,
# sehingga BaseContext.__copy__() yang memanggil copy(super()) akan error:
# "AttributeError: 'super' object has no attribute 'dicts'"
# Patch ini mengganti method __copy__ dengan versi yang kompatibel.
import sys
if sys.version_info >= (3, 14):
    try:
        from copy import copy
        from django.template.context import BaseContext

        def _patched_base_context_copy(self):
            duplicate = self.__class__.__new__(self.__class__)
            duplicate.__dict__.update(self.__dict__)
            duplicate.dicts = self.dicts[:]
            return duplicate

        BaseContext.__copy__ = _patched_base_context_copy
    except Exception:
        pass

