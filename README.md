<p align="center"> <img src="https://raw.githubusercontent.com/qeeqbox/analyzer/master/readme/analyzerlogo.png"></p>

This project automates the daily tasks of Threat Intelligence Analyzer role **internally** without external resources' interaction. It analyzes, visualizes and structures **sensitive** files (Malware) or data by extracting features, artifacts and IoC using different modules. The output of those modules can be easily integrated in your research or SOC platforms.

## Install
```git clone https://github.com/qeeqbox/analyzer.git && cd analyzer &&  chmod +x run.sh && ./run.sh auto_configure```

## Interface
<img src="https://raw.githubusercontent.com/qeeqbox/analyzer/master/readme/intro.gif" style="max-width:768px"/>

## Output 
- [APT-Malware JSON\HTML reports (+190 sample)](https://files.qeeqbox.com/set1/)

## Features
- Runs locally (Offline)  
- Analyze buffer, file or full folder  
- Intime analysis (Session is saved)  
- 2 modes (Interactive and silent)  
- Generates HTML or JSON as output  
- Dump output file with details to mongodb  
- Save raw json result to mongodb  
- Basic file information MD5, charset, mime, ssdeep  
- Different string/patterns analysis methods  
- Web service and API  
- Ports, IPS hints and countries description  
- World IPS world image and flags  
- DNS servers description (Top servers)  
- Artifacts force directed image  
- Cross references force directed image and table  
- Similarity image divided to classes  
- YARA module, and YARA rules from yara-rules-github)  
- YARA module includes conditions & tags by index  
- Whitelist implemented (Windows7, 8 and 10 files)  
- Check WAF and bypass proxy  
- Spelling and punctuation check  
- Top phishing words included  
- Snort support  
- PDF, RTF, Phishing, MS office and HTML modules  
- NL English words detection  
- OCR words detection  
- Websites similarity detection (Top 10000)  
- BOM (Byte Order Mark) detection  
- MITRE att&ck tools and patterns detection (could be FP)  
- URL shorteners extraction  
- ASCII from UNICODE extraction  
- Free\Fake email extraction  
- URL, EMAIL, and TEL Tags patterns extraction  
- Credit Cards, Credential, and Secrets patterns patterns extraction  
- Encryption patterns (base64, md5, sha1..) extraction  
- DGA (Domain Generation Algorithm) patterns extraction  


## One click auto-configure
```bash
git clone https://github.com/qeeqbox/analyzer.git
cd analyzer
chmod +x run.sh
./run.sh auto_configure
The project interface http://127.0.0.1:8000/login/ will open automatically after finishing the initialization process
```

## Or, if you already have docker-compose
```bash
docker-compose -f docker-compose-dev.yml up --build
Then open http://127.0.0.1:8000/login/
```

## Prerequisites
apt-get install -y python3 python3-pip curl libfuzzy-dev yara libmagic-dev libjansson-dev libssl-dev libffi-dev tesseract-ocr libtesseract-dev libssl-dev swig p7zip-full radare2 dmg2img mongodb redis

pip3 install pyelftools macholib python-magic nltk Pillow jinja2 ssdeep pefile scapy r2pipe pytesseract M2Crypto requests tld tldextract bs4 psutil pymongo flask pyOpenSSL oletools extract_msg

Prerequisites packages are required for some modules (If you are having issues using those packages, I might be able to share with you my own alternatives that I developed in the past in C#\C)

## Roadmap
- Java analysis (Requested by users)
- Web detection
- Adding username and password wrappers to databases
- CSS clean up

## Resources
Linux documentation, MacOS documentation, Windows documentation, Android documentation, software77, MITRE ATT&CK™, sc0ty, hexacorn, PEID, steren, bacde, cisco umbrella , yara rules community , TONS OF RESEARCHES

## Other Licenses
By using this framework, you are accepting the license terms of all these packages: yara, Yara-Rules, tesseract-ocr, swig, radare, vu1tur, oletools, mongodb, supervisor, msg-extractor, snort, pyelftools, macholib, pefile, scapy, python-magic, flask, werkzeug, gunicorn, flask-mongoengine, flask-admin, flask-login, flask-bcrypt, pyopenssl, flask-markdown, tld, psutil, gevent, dateutil, requests, pymongo, BeautifulSoup, tldextract, m2crypto, radare2, ssdeep, jinja2, Pillow, nltk, p7zip, redislabs, redis-py

## Disclaimer\Notes
- Do not deploy without proper configuration
- Setup some security group rules and remove default credentials
- This project is NOT an anti malware project and does not quarantine or delete malicious files
- This project was developed for analyzing classified data and training some AI locally without internet/external interaction
- Please let me know if i missed a resource or dependency

## Other Projects
[![](https://github.com/qeeqbox/.github/blob/main/data/social-analyzer.png)](https://github.com/qeeqbox/social-analyzer) [![](https://github.com/qeeqbox/.github/blob/main/data/chameleon.png)](https://github.com/qeeqbox/chameleon) [![](https://github.com/qeeqbox/.github/blob/main/data/honeypots.png)](https://github.com/qeeqbox/honeypots) [![](https://github.com/qeeqbox/.github/blob/main/data/osint.png)](https://github.com/qeeqbox/osint) [![](https://github.com/qeeqbox/.github/blob/main/data/url-sandbox.png)](https://github.com/qeeqbox/url-sandbox) [![](https://github.com/qeeqbox/.github/blob/main/data/mitre-visualizer.png)](https://github.com/qeeqbox/mitre-visualizer) [![](https://github.com/qeeqbox/.github/blob/main/data/woodpecker.png)](https://github.com/qeeqbox/woodpecker) [![](https://github.com/qeeqbox/.github/blob/main/data/docker-images.png)](https://github.com/qeeqbox/docker-images) [![](https://github.com/qeeqbox/.github/blob/main/data/seahorse.png)](https://github.com/qeeqbox/seahorse) [![](https://github.com/qeeqbox/.github/blob/main/data/rhino.png)](https://github.com/qeeqbox/rhino) [![](https://github.com/qeeqbox/.github/blob/main/data/raven.png)](https://github.com/qeeqbox/raven) [![](https://github.com/qeeqbox/.github/blob/main/data/image-analyzer.png)](https://github.com/qeeqbox/image-analyzer)

