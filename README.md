# CashSign Server

CashSign server is an example application to demonstrate how you may utilize the CashSign protocol to implement a single sign on, by requesting your wallet to sign a special message. 

## Install 

```
pip install -r requirements.txt
./init.sh

# modify config to support rpc
$(EDITOR) ~/.electron-cash/config

# start daemon and load correct wallet
electron-cash daemon start
electron-cash daemon load_wallet -w ~/.electron-cash/wallets/default_wallet
```


# test using

```
electron-cash signmessage bitcoincash:qpycfdu0s5ek5ypu6ekwr2wkj5d8l9ffyujykcg0dn "message that will be signed"
```

Retrieve the sigdata and call:

http://127.0.0.1:5000/cashsign-callback?address=qraycjp6ukmexm6xrychfzqxxc0cv3qkeglxjp9kec&payload=HwPT1GxS+x/CJnwt8n+gw7xJK7ejTg20n4QSXPcsShlbLxJ/srLfEPOfe5SR0/fKhieRHeIuieqpiE6r7GS4lB4=
