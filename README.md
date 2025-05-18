# DNS-BOMBER 🚀🧨

**DNS-BOMBER** is a high-speed, multi-protocol attack simulation tool designed for **penetration testing**, **network analysis**, and **educational purposes** only. It can simulate HTTP floods, TCP/UDP floods, and DNS amplification-style traffic.

> ⚠️ **DISCLAIMER**  
> This tool is intended for **authorized testing** and **educational use** only.  
> Misuse may result in **legal consequences**. Always obtain **explicit permission** before targeting any system.

---

## Features ✨

- 🔁 Multi-threaded attack execution
- 🌐 HTTP/HTTPS flood with randomized headers & spoofed IPs
- 🧬 DNS amplification simulation
- 🔌 TCP/UDP payload flooding
- 🛠️ IPv4 and IPv6 spoofing
- 📝 Color-coded logging for better readability

---

## Installation ⚙️

1. Clone the repository:
```bash
git clone https://github.com/ciphersquid666/DNS-BOMBER
cd DNS-BOMBER

2. Install dependencies:



pip install -r requirements.txt


---

Usage 🕹️

Run the main script:

python ZeroDNS.py

Interactive Options

Prompt	Description	Example

Target	Target IP/Host and port	example.com:80
Method	Type of attack method	HTTP, DNS, TCP
Duration	Attack duration in seconds	60
RPS (Requests Per Second)	Number of threads/requests per second	50
IP Version	IP version used for spoofing	4 or 6



---

Attack Methods 🧪

Method	Description

HTTP	Sends HTTP requests with spoofed IPs
TCP	TCP socket flood with fake payloads
UDP	UDP packet flood with spoofed IPs
DNS	Simulated DNS amplification



---

Example Session 🧾

Welcome by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙 
Enter the target (IP:PORT or URL): example.com:443
Enter the attack method (HTTP, HTTPS, TCP, UDP, DNS): HTTP
Enter the attack duration in seconds: 120
Enter the number of requests per second (RPS): 100
Enter the IP version (4 for IPv4, 6 for IPv6): 4


---

Contribution 🤝

Feel free to fork, modify, or submit pull requests to improve this tool.

To contribute:

1. Fork this repository


2. Create your feature branch (git checkout -b feature/your-feature)


3. Commit your changes (git commit -m 'Add new feature')


4. Push to the branch (git push origin feature/your-feature)


5. Create a new Pull Request




---

License 📄

This project is licensed under the MIT License.
See the LICENSE file for details.


---

Author 🐙

Cipher Squid
GitHub: @ciphersquid666

> Keep your tests ethical. Stay legal. Hack responsibly.
