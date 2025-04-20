#!/usr/bin/env python3
#coding: utf-8
# forenum_O365 v1.1 (20_04_2025)
# By Gustavo Segundo (@Bytenull%00)
# Please use responsibly...
# Contact: gasso2do@gmail.com
# https://www.linkedin.com/in/gustavosegundo/

import requests
import time
import argparse
import sys
import socket
from datetime import datetime
from stem import Signal
from stem.control import Controller
import os
import random
import pyfiglet

use_tor = False
use_gateway = False
proxies = None

def listening(host, port):
    try:
        socket.create_connection((host, port), timeout=3).close()
        return True
    except:
        return False

def verify_tor():
    return listening('127.0.0.1', 9050)

def control_tor():
    return listening('127.0.0.1', 9051)

def get_ip_tor():
    try:
        r = requests.get("https://icanhazip.com", proxies=proxies, timeout=10)
        return r.text.strip()
    except Exception as e:
        print(f"[!] Error obtaining IP via Tor: {e}")
        return None

def change_ip_tor(ip_before):
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("[*] Requesting a new Tor IP...")
        time.sleep(5)
        new_ip = get_ip_tor()
        attempts = 0
        while new_ip == ip_before and attempts < 5:
            time.sleep(5)
            new_ip = get_ip_tor()
            attempts += 1
        if new_ip != ip_before:
            print(f"[+] New IP: {ip_before} -> {new_ip}")
        else:
            print("[!] Failed to change IP after several attempts")
        return new_ip
    except Exception as e:
        print(f"[!] Error changing IP: {e}")
        return ip_before

def cargar_gateways(nombre_archivo):
    try:
        with open(nombre_archivo) as f:
            lineas = [line.strip() for line in f if line.strip()]
            if len(lineas) < 2:
                print(f"[!] The file {nombre_archivo} must contain at least 2 endpoints to allow rotation")
                sys.exit(1)
            return lineas
    except FileNotFoundError:
        print(f"[!] file not found: {nombre_archivo}")
        sys.exit(1)


def validar_getcredentialtype(correo, ms_url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    data = { "Username": correo }
    try:
        r = requests.post(ms_url, headers=headers, json=data, proxies=proxies, timeout=10)
        resultado = r.json()
        return resultado.get("IfExistsResult", -1)
    except Exception as e:
        print(f"[!] {correo} error GetCredentialType: {e}")
        return -1


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("forenum_O365")
    print(ascii_banner)
    print("                             v1.1")
    print("            By Gustavo Segundo | gasso2do@gmail.com | @Bytenull%00\n")
    parser = argparse.ArgumentParser(description="Email validator in Microsoft 365")
    parser.add_argument("file", help="File with list of users")
    parser.add_argument("--domain", required=True, help="Domain")
    parser.add_argument("--rotate", required=True, type=int, help="Change IP every N attempts")
    parser.add_argument("--delay", required=True, type=float, help="Delay between attempts in seconds")
    parser.add_argument("--force", action="store_true", help="Ignore previous progress and start from scratch")
    parser.add_argument("--tor", action="store_true", help="Use Tor proxy")
    parser.add_argument("--api", action="store_true", help="Use AWS API Gateway rotation")
    parser.add_argument("--gateways", help="File with API Gateway endpoints (required if --api)")
    args = parser.parse_args()

 
    if args.tor and args.api:
        print("[!] You can't use both --tor and --api")
        sys.exit(1)


    if args.api:
        if not args.gateways:
            print("[!] You must provide the gateways file using --gateways if you enable --api")
            sys.exit(1)
        gateways = cargar_gateways(args.gateways)
        if args.rotate > len(gateways):
            print(f"[!] The value of --rotate {args.rotate} cannot be greater than the number of gateways {len(gateways)}")
            sys.exit(1)
        use_gateway = True
        ms_url = random.choice(gateways)
        print(f"[*] Rotating gateway: {ms_url}")
    else:
        ms_url = "https://login.microsoftonline.com/common/GetCredentialType"


    if args.tor:
        use_tor = True
        if not verify_tor():
            print("[-] Tor SOCKS5 proxy not available (127.0.0.1:9050)")
            sys.exit(1)
        if not control_tor():
            print("[-] Tor control unavailable (127.0.0.1:9051)")
            sys.exit(1)
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        ip_current = get_ip_tor()
        if not ip_current:
            print("[-] Failed to obtain Tor IP")
            sys.exit(1)
        print(f"[*] Current Tor IP: {ip_current}")

    try:
        with open(args.file) as f:
            users = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {args.file}")
        sys.exit(1)

    progress_file = f"processed_{args.domain.replace('.', '_')}.log"
    output_file = f"valid_{args.domain.replace('.', '_')}.txt"

    already_processed = set()
    if args.force:
        print("[!] Forced mode enabled. Progress file will be ignored if it exists")
        if os.path.exists(progress_file):
            os.remove(progress_file)
    else:
        try:
            with open(progress_file) as f:
                already_processed = set(line.strip().split()[0] for line in f if line.strip())
                print(f"[*] Found {len(already_processed)} users already processed")
        except FileNotFoundError:
            print(f"[i] File not found {progress_file}. Starting from scratch")

    all_users = [u if "@" in u else f"{u}@{args.domain}" for u in users]
    pending = [c for c in all_users if c not in already_processed]

    valid_emails = set()
    try:
        with open(output_file) as f:
            valid_emails = set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        pass

    try:
        for i, email in enumerate(pending, 1):
            
            if args.api and i % args.rotate == 0:
                ms_url = random.choice(gateways)
                print(f"[*] Rotating gateway → {ms_url}")

            result = validar_getcredentialtype(email, ms_url)

            with open(progress_file, "a") as log:
                if result == 0:
                    print(f"[+] {email} valid", flush=True)
                    if email not in valid_emails:
                        with open(output_file, "a") as f:
                            f.write(email + "\n")
                        valid_emails.add(email)
                    log.write(f"{email} valid\n")
                elif result == 1:
                    print(f"[-] {email} not valid", flush=True)
                    log.write(f"{email} not_valid\n")
                elif result == 5:
                    print(f"[?] {email} federated", flush=True)
                    log.write(f"{email} federated\n")
                else:
                    print(f"[?] {email} unknown code: {result}", flush=True)
                    log.write(f"{email} unknown\n")

            time.sleep(args.delay)

            
            if args.tor and i % args.rotate == 0:
                ip_current = change_ip_tor(ip_current)

    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user. Exiting...")

    print(f"\n[*] Valid emails saved in: {output_file}")
