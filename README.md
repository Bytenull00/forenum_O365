# forenum_O365

This tool allows you to enumerate email accounts in Office 365 by passing a list of possible usernames and the domain to test.

### Requirements

This tool uses the common libraries that come natively in Python 3.9.2+, however it requires some additional libraries for aesthetic purposes.

### Installation

Installing 

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

![image](https://github.com/user-attachments/assets/c438b9e1-92b1-40e5-92d8-e8e9d8a37029)


### Credits 

* Gustavo Segundo - ByteNull%00 - gasso2do@gmail.com
