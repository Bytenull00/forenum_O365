# forenum_O365

This tool allows you to enumerate email accounts in Office 365 by passing a list of possible usernames and the domain to test. The goal is to obtain a list of valid emails for later password spraying.

One of the key features of this tool is that it allows IP rotation through the TOR network after a specified number of attempts, as well as a delay between each request to avoid detection or blocking.

Additionally, the tool resumes enumeration from where it left off by checking previously processed users, ensuring no duplicates are queried.

## Versions

- `v1.0`: Validation using IP rotation with Tor
- `v1.1`: Now also supports rotation using multiple AWS API Gateways

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
usage: forenum_O365.py [-h] --domain DOMAIN --rotate ROTATE --delay DELAY [--force] [--tor] [--api] [--gateways GATEWAYS] file

Email validator in Microsoft 365

positional arguments:
  file                 File with list of users

options:
  -h, --help           show this help message and exit
  --domain DOMAIN      Domain
  --rotate ROTATE      Change IP every N attempts
  --delay DELAY        Delay between attempts in seconds
  --force              Ignore previous progress and start from scratch
  --tor                Use Tor proxy
  --api                Use AWS API Gateway rotation
  --gateways GATEWAYS  File with API Gateway endpoints (required if --api)

```

# Results

The script queries the GetCredentialType endpoint and displays the results based on the values returned.

| Code  | Meaning     | Technical Description |
|-------|-------------|------------------------|
| `0`   | **Valid**     | The email address exists in Microsoft 365. |
| `1`   | **Invalid**  | The email address does not exist in Microsoft 365. |
| `5`   | **Federated** | The domain is federated. Authentication is handled via ADFS or another external identity provider, so Microsoft cannot confirm whether the user exists. |
| Other | **Unknown** | An undocumented value was received. The script labels it as "unknown". |

# Demo

![image](https://github.com/user-attachments/assets/16ea16f8-b39d-439f-aee4-3dad445810b2)

![image](https://github.com/user-attachments/assets/928a4b31-3eb6-4970-bc7c-308b20584d34)

![image](https://github.com/user-attachments/assets/3e4555f4-45ad-4c40-b1a7-ad28da6dda57)

![image](https://github.com/user-attachments/assets/5ce751b9-d4dd-43b5-9f37-c39e255ccc5d)



### Credits 

* Gustavo Segundo - ByteNull%00 - gasso2do@gmail.com
* https://www.linkedin.com/in/gustavosegundo/ 
