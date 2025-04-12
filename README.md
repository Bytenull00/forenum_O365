# forenum_O365

This tool allows you to enumerate email accounts in Office 365 by passing a list of possible usernames and the domain to test. The goal is to obtain a list of valid emails for later password spraying.

One of the key features of this tool is that it allows IP rotation through the TOR network after a specified number of attempts, as well as a delay between each request to avoid detection or blocking.

Additionally, the tool resumes enumeration from where it left off by checking previously processed users, ensuring no duplicates are queried.

### Requirements

```
sudo apt update
sudo apt install tor
```

### Configuration

Edit the configuration file
```
sudo nano /etc/tor/torrc
```
Add the following lines to the end of the file

```
SOCKSPort 9050
ControlPort 9051
CookieAuthentication 1
```
Start the TOR service

```
sudo systemctl start tor@default
```

### Installation

```
pip3 install -r requirements.txt
python3 forenum_O365.py --help
```

# Usage 

```
usage: forenum_O365.py [-h] --domain DOMAIN --rotate ROTATE --delay DELAY [--force] file

Email validator in Microsoft 365

positional arguments:
  file             File with list of users

options:
  -h, --help       show this help message and exit
  --domain DOMAIN  Domain
  --rotate ROTATE  Change IP every N attempts
  --delay DELAY    Delay between attempts in seconds
  --force          Ignore previous progress and start from scratch

```

# Demo

![image](https://github.com/user-attachments/assets/16ea16f8-b39d-439f-aee4-3dad445810b2)

![image](https://github.com/user-attachments/assets/928a4b31-3eb6-4970-bc7c-308b20584d34)

![image](https://github.com/user-attachments/assets/984e74be-2653-4d40-aa78-be0b33739d6f)

![image](https://github.com/user-attachments/assets/c438b9e1-92b1-40e5-92d8-e8e9d8a37029)


### Credits 

* Gustavo Segundo - ByteNull%00 - gasso2do@gmail.com
