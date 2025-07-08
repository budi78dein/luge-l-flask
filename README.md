# Lugel Flask App

Aplikasi login/register Flask dengan:
- Validasi password
- Upload foto profil
- Simpan user ke SQLite
- Tampilan Bootstrap
- Bisa diakses dari internet via Render.com

## Cara Deploy ke Render

1. Upload semua file ini ke GitHub (nama repo bebas)
2. Buat akun di https://render.com dan login
3. Klik "New Web Service" > "Deploy from GitHub"
4. Pilih repo ini
5. Render akan otomatis deploy dengan `app.py` sebagai entry point

URL akhir kamu akan seperti:
```
https://lugel-app.onrender.com
```

## Struktur Folder

```
app.py
requirements.txt
render.yaml
templates/
  login.html
  register.html
  profile.html
static/uploads/
```