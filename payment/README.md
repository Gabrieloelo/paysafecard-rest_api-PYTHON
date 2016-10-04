# Paysafecard payment api Python class & example

You need to have requests installed.

```
pip install requests
```

for more information see: http://docs.python-requests.org/en/master/user/install/#install


## minimal basic usage

```python
#import payment Class
from PSCPayment import PSCPayment
import socket
import json # for proper dumping

# your psc key
key = 'psc_xl0EwfLX-96bEkjy-mXYD7SFviyvaqA'

#test payment id
payment_id = 'pay_1000005843_D4Lp2baNCH1QHwV9aIPzs7k1fBIPd2mY_EUR'

# set the environment: TEST or PRODUCTION
environment = 'TEST'

# create pscpayment instance
pscpayment = PSCPayment(key, environment)


# Variables

# amount of this payment, i.e. 10.00
amount = 0.10

# currency of this payment, i.e. 'EUR'
currency = 'EUR'

# customer ID (merchant client ID)
customer_id = 'test123456'

# the customers IP (not your server IP)
customer_ip = socket.gethostbyname(socket.gethostname())

# URL to redirect the customer to after a successful payment
success_url = 'http://www.yoururl.com/success.php?payment_id={payment_id}'

# URL to redirect the customer to after a failed payment
failure_url = 'http://www.yoururl.com/failure.php?payment_id={payment_id}'

# URL to call by the psc API to notify your scripts of the payment
notification_url = 'http://www.yoururl.com/notification.php?payment_id={payment_id}'
"""
create a payment
"""
pscpayment.createPayment(amount , currency, customer_id, customer_ip, success_url, failure_url, notification_url)

if pscpayment.requestIsOK():
    # check if the createpayment request was successful

    # redirect customer to payment page
    print 'Redirect to (for testing open in browser): ' + pscpayment.getResponse()['redirect']['auth_url']

else:
    # create payment failed, handle errors
    error = pscpayment.getError()
    print "#### Error ####"
    print "Create Request failed with Error: " + str(error['number']) + " - "+  error['message']
    print json.dumps(pscpayment.getResponse(), indent=2)

"""
retrieve a payment
"""
pscpayment.retrievePayment(payment_id)

# check if retrieve request was successful
if pscpayment.requestIsOK():
    # capture was successful
    print 'Retrieve request was successful. check for status and proceed. Reponse:'
    print json.dumps(pscpayment.getResponse(), indent=2)
else:
    # capture failed
    error = pscpayment.getError()
    print "#### Error ####"
    print "Retrieve Request failed with Error: " + str(error['number']) + " - "+  error['message']
    print json.dumps(pscpayment.getResponse(), indent=2)



"""
capture a payment
"""
pscpayment.capturePayment(payment_id)

# check if capture request was successful
if pscpayment.requestIsOK():
    # capture was successful
    print 'Capture request was successful. check for status and proceed. Reponse:'
    print json.dumps(pscpayment.getResponse(), indent=2)
else:
    # capture failed
    error = pscpayment.getError()
    print "#### Error ####"
    print "Capture Request failed with Error: " + str(error['number']) + " - "+  error['message']
    print json.dumps(pscpayment.getResponse(), indent=2)

```

## for a more advanced example have a look into payment_example.py
