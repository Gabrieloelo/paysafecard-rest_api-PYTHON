# Paysafecard payment api Python class & example

You need to have requests installed.

```
pip install requests
```

for more information see: http://docs.python-requests.org/en/master/user/install/#install


## minimal basic usage

```python
#import payout class
from PSCPayout import PSCPayout
import json # for proper dumping

# your psc key
key = 'psc_xl0EwfLX-96bEkjy-mXYD7SFviyvaqA'

# set the environment: TEST or PRODUCTION
environment = 'TEST'

# create pscpayout instance
pscpayout = PSCPayout(key, environment)



# Variables

# amount of this payout, i.e. 10.00
amount = 0.10

# currency of this payout, i.e. 'EUR'
currency = 'EUR'

# customer ID (merchant client ID)
customer_id = '434186408713'

# customer mail to payout to (psc)
customer_email = 'VrAtTRLRyS@avUVWdRVeH.NYE'

# the customers IP (not your server IP)
customer_ip = '123.123.123.123'

# first_name
first_name = 'Test'

# Last Name
last_name = 'BubxNFGHwdGCElzbmjxsycWdYX'

# Date of Birth
birthday = '1986-06-16'

"""
get limits
"""
print 'get Limits:'
pscpayout.getLimits('EUR')

if pscpayout.requestIsOK():
    # check if the request was successful
    print "Limits Request successful. Response:"
    print json.dumps(pscpayout.getResponse(), indent=2)

else:
    # Limit request failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "Limit Request failed with Error: " + str(error['number']) + " - "+  error['message']


"""
validate a payout
"""
### validate a payout
pscpayout.validatePayout(amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday)

if pscpayout.requestIsOK():
    # check if the request was successful
    print "Validate Request successful."
    if pscpayout.getResponse()['status'] == 'VALIDATION_SUCCESSFUL':
        print 'Validation was successful.'
        print json.dumps(pscpayout.getResponse(), indent=2)
    else:
        print json.dumps(pscpayout.getResponse(), indent=2)

else:
    # validate payout failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']


"""
execute a Payout
"""
## For usage information: have a look at validatePayout above, since they both use the same variables
pscpayout.executePayout(amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday)

if pscpayout.requestIsOK():
    # check if the request was successful
    print "execute Request succeeded:"
    if pscpayout.getResponse()['status'] == 'SUCCESS':
        # executtion of payout was successful
        print 'Execution was successful. Payout successful'
        print json.dumps(pscpayout.getResponse(), indent=2)
    else:
        print json.dumps(pscpayout.getResponse(), indent=2)

else:
    # execute payout failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']

```

## for a more advanced example have a look into payout_example.py
