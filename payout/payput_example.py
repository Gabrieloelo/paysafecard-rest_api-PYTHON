#import payout class
from PSCPayout import PSCPayout
import socket
import uuid
import json # for proper dumping


#debug
debug = False

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
customer_ip = socket.gethostbyname(socket.gethostname())

# first_name
first_name = 'Test'

# Last Name
last_name = 'BubxNFGHwdGCElzbmjxsycWdYX'

# Date of Birth
birthday = '1986-06-16'

## optional features for advanced usage
#
## Define a unique identifier for referencing (optional) default is None
# default: None
# max length: 41
#correlation_id = str(uuid.uuid4())
#correlation_id = 'uniq_id_123'
#
## Reporting Criteria
# default: None
#submerchant_id = 1
#
# Usage:
#pscpayout.validatePayout(amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday, correlation_id, submerchant_id)
#




## get limits

## for limit information
print '###############'
raw_input("Press Enter to request limit informations...")
pscpayout.getLimits('EUR')
print(pscpayout.getResponse())

if pscpayout.requestIsOK():
    # check if the request was successful
    print "Limits Request successful."
    if debug:
        ## for debugging / more information show response:
        print "Request Parameter:"
        print json.dumps(pscpayout.getRequestPrameter(), indent=2)
        print "Request Info:"
        print(pscpayout.getRequestInfo())
        print "Reqest Limit Response:"
        print json.dumps(pscpayout.getResponse(), indent=2)
else:
    # Limit request failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "Limit Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'debug Response:'
        print json.dumps(pscpayout.getResponse(), indent=2)
        print "###############"

## print limits
print 'Limits:'
print json.dumps(pscpayout.getResponse(), indent=2)


## validate Payout info
print '###############'
raw_input("Press Enter to continue to validate payout...")



# validate a payout
pscpayout.validatePayout(amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday)

if pscpayout.requestIsOK():
    # check if the request was successful
    print "Validate Request successful."
    if pscpayout.getResponse()['status'] == 'VALIDATION_SUCCESSFUL':
        print 'Validation was successful.'
    else:
        print json.dumps(pscpayout.getResponse(), indent=2)

    if debug:
        ## for debugging / more information show response:
        print "Request Parameter:"
        print json.dumps(pscpayout.getRequestPrameter(), indent=2)
        print "Request Info:"
        print(pscpayout.getRequestInfo())
        print "Validate payout Response:"
        print json.dumps(pscpayout.getResponse(), indent=2)
else:
    # validate payout failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'debug Response:'
        print json.dumps(pscpayout.getResponse(), indent=2)
        print "###############"



## execute a Payout
print '###############'
raw_input("Press Enter to continue to execute payout...")

## For usage information: have a look at validatePayout above, since they both use the same variables
pscpayout.executePayout(amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday)

if pscpayout.requestIsOK():
    # check if the request was successful
    print "execute Request succeeded:"
    if pscpayout.getResponse()['status'] == 'SUCCESS':
        # executtion of payout was successful
        print 'Execution was successful. Payout successful'
    else:
        print(pscpayout.getRequestPrameter())

    if debug:
        ## for debugging / more information show response:
        print "Request Parameter:"
        print json.dumps(pscpayout.getRequestPrameter(), indent=2)
        print "Request Info:"
        print(pscpayout.getRequestInfo())
        print "execute payout Response:"
        print json.dumps(pscpayout.getResponse(), indent=2)
else:
    # execute payout failed, handle errors
    error = pscpayout.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'debug Response:'
        print json.dumps(pscpayout.getResponse(), indent=2)
        print "###############"


print '######## Test finished #######'
