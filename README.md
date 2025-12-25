# Jaring Pengintai (HTTP Packet Sniffer)

Sebuah alat keamanan siber (*Network Sniffing Tool*) sederhana berbasis Python. Alat ini mendemonstrasikan bahaya menggunakan protokol **HTTP** (tanpa enkripsi) di jaringan publik.

Alat ini mampu mencegat lalu lintas jaringan secara *real-time* dan mengekstrak informasi sensitif seperti URL yang dikunjungi serta Username dan Password yang dikirim dalam bentuk teks biasa (*clear text*).

## Fitur Utama
* **Real-time Monitoring:** Memantau aktivitas browsing pada jaringan lokal.
* **Credential Harvesting:** Mendeteksi dan menangkap data login (POST Request) yang tidak terenkripsi.
* **Filter HTTP:** Secara otomatis memisahkan lalu lintas HTTP dari data jaringan lainnya.

## Prasyarat
* Python 3.x
* Hak Akses Administrator/Root (Wajib untuk akses kartu jaringan mode *promiscuous*).

## Instalasi
1. Clone repositori ini:
   git clone [https://github.com/code-GiL/HTTP-packet-sniffer.git](https://github.com/code-GiL/HTTP-packet-sniffer.git)
   cd jaring-pengintai
2. Install library yang dibutuhkan
    pip install -r requirements.txt

## Cara Penggunaan
1. Cek Interface Jaringan
Cek nama interface WiFi Anda menggunakan perintah ifconfig (Mac/Linux) atau ipconfig (Windows).
Biasanya en0 pada macOS.
Biasanya wlan0 atau eth0 pada Linux.
Catatan: Edit baris interface_wifi di dalam file pengintai.py jika perlu.
2. Jalankan Program
Gunakan sudo karena sniffing membutuhkan akses level rendah ke hardware.
    sudo python3 pengintai.py
3. Pengujian (Wajib Baca)
Alat ini TIDAK AKAN bekerja pada website HTTPS (Google, Facebook, Twitter) karena datanya terenkripsi.
Untuk menguji apakah alat ini bekerja, gunakan website tes kerentanan berikut: 👉 http://testphp.vulnweb.com/login.php
- Buka link di atas.
- Masukkan username/password asal (misal: admin/rahasia123).
- Lihat terminal Anda, data tersebut akan muncul.

## Disclaimer Hukum 
Alat ini dibuat semata-mata untuk tujuan EDUKASI dan KESADARAN KEAMANAN. Menggunakan alat ini untuk memantau jaringan orang lain tanpa izin adalah tindakan ilegal (Penyadapan/Interception) dan melanggar UU ITE. Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.

# Lisensi
MIT License