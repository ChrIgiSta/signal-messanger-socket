## A HTTP Server to send Messages over Signal Messager
This docker container provides a HTTP Server on Port 16323 to recieve a HTTP Post to send a Message over Signal Messanger using the signal-cli `https://github.com/AsamK/signal-cli.git` from `AsamK`.

## How to use

### Install
 * set your own phone number by modifing `OWN_PHONE_NUMBER` in `signal_socket.py`
 * install docker and docker-compose on your machine and run `docker-compose up --detach`

### Register a phone
 * register a number by sending a HTTP Post to `localhost:16323/reg`
   * e.g. use curl 
```[shell]
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"value1":"","value2":"","value3":""}' \
  -X POST http://localhost:16323/reg
```

 * verify your phone number by sending a HTTP Post to `localhost:16323/verify` with content type `application/json` and content `{"value1":"verificationCodeSendedBySms"}`
   * e.g. use curl
```[shell]
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"value1":"verificationCodeSendedBySms","value2":"","value3":""}' \
  -X POST http://localhost:16323/verify
```

### Send a Signal Message
 * send a message over signal sending a HTTP Post to `localhost:16323/sms` with content type `application/json` and content `{"value1":"receiptPhoneNumber","value2":"yourMessageText"}`
   * e.g. use curl
```[shell]
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"value1":"receiptPhoneNumber","value2":"yourTextToSend","value3":""}' \
  -X POST http://localhost:16323/sms
```

