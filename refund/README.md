# Paysafecard payment api Python class & example

You need to have requests installed.

```
pip install requests
```

for more information see: http://docs.python-requests.org/en/master/user/install/#install


## minimal basic usage

```python
#import refund class
from PSCRefund import PSCRefund
import uuid
import json # for proper dumping

# your psc key
key = 'psc_xl0EwfLX-96bEkjy-mXYD7SFviyvaqA'

# set the environment: TEST or PRODUCTION
environment = 'TEST'

# create pscrefund instance
pscrefund = PSCRefund(key, environment)

# payment id to refund
payment_id = 'pay_1000005843_testCorrID_5780325650790_EUR'


## get payment Detail
pscrefund.getPaymentDetail(payment_id)

if pscrefund.requestIsOK():
    # check if the request was successful
    print "Get Payment Details Request succeeded:"
    print json.dumps(pscrefund.getResponse(), indent=2)
else:
    # Get Payment Details failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "Get Payment Details Request failed with Error: " + str(error['number']) + " - "+  error['message']



# Variables

# set payment id, use from payment details
payment_id = pscrefund.getResponse()['id']

# amount to refund, i.e. 1.00
amount = 0.01

# currency of this payment, i.e. 'EUR', use from payment details
currency = pscrefund.getResponse()['currency']

# customer ID (merchant client ID), use from payment details
customer_id = pscrefund.getResponse()['customer']['id']

# customer mail to refund to (psc)
customer_email = 'psc.mypins+matwal_blFxgFUJfbNS@gmail.com'

# the customers IP (not your server IP)
customer_ip = '123.123.123.123'

"""
Validate a Refund
"""
pscrefund.validateRefund(payment_id, amount, currency, customer_id, customer_email, customer_ip)
if pscrefund.requestIsOK():
    # check if the request was successful
    print "Validate request succeeded:"
    print json.dumps(pscrefund.getResponse(), indent=2)
else:
    # payment failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']


"""
Execute a Refund
"""
## For usage information have a look at validate Refund above
# use refund ID and necessary Information from the prior validation
pscrefund.executeRefund(payment_id, pscrefund.getResponse()['id'], pscrefund.getResponse()['amount'], pscrefund.getResponse()['currency'], pscrefund.getResponse()['customer']['id'], pscrefund.getResponse()['customer']['email'], customer_ip)

if pscrefund.requestIsOK():
    # check if the request was successful
    print "Execute Request succeeded:"
    print json.dumps(pscrefund.getResponse(), indent=2)
else:
    # Refund failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "Execute Request failed with Error: " + str(error['number']) + " - "+  error['message']

"""
Execute a direct Refund
"""
## For usage information have a look above
pscrefund.directRefund(payment_id, amount, currency, customer_id, customer_email, customer_ip)

if pscrefund.requestIsOK():
    # check if the request was successful
    print "Direct refund Request succeeded."
    print json.dumps(pscrefund.getResponse(), indent=2)
else:
    #  direct Refund failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']

```

## for a more advanced example have a look into refund_example.py
