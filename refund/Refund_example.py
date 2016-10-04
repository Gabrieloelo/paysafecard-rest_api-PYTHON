#import refund class
from PSCRefund import PSCRefund
import uuid
import json # for proper dumping

#debug
debug = False

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
    if pscrefund.getResponse()['status'] == 'SUCCESS':
        print 'Get Payment Details was successful. Details:'
        print json.dumps(pscrefund.getResponse(), indent=2)
    else:
        print 'Get Payment Details. Response:'
        print json.dumps(pscrefund.getResponse(), indent=2)
    if debug:
        ## for debugging / more information show response:
        print "Execute Request Parameter:"
        print json.dumps(pscrefund.getRequestPrameter(), indent=2)
        print "Execute Request Info:"
        print(pscrefund.getRequestInfo())
        print "Execute Refund Response:"
        print json.dumps(pscrefund.getResponse(), indent=2)
else:
    # Get Payment Details failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "Get Payment Details Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'Get Payment Details debug Response:'
        print json.dumps(pscrefund.getResponse(), indent=2)
        print "###############"






## validate Refund
print '###############'
raw_input("Press Enter to continue to validate Refund...")

# Variables

# set payment id
payment_id = pscrefund.getResponse()['id']

# amount to refund, i.e. 1.00
amount = 0.01

# currency of this payment, i.e. 'EUR'
currency = pscrefund.getResponse()['currency']

# customer ID (merchant client ID)
customer_id = pscrefund.getResponse()['customer']['id']

# customer mail to refund to (psc)
customer_email = 'psc.mypins+matwal_blFxgFUJfbNS@gmail.com'

# the customers IP (not your server IP)
customer_ip = '123.123.123.123'

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
#pscrefund.validateRefund(payment_id, amount, currency, customer_id, customer_email, customer_ip, correlation_id, submerchant_id)
#
# validate a Refund


pscrefund.validateRefund(payment_id, amount, currency, customer_id, customer_email, customer_ip)

if pscrefund.requestIsOK():
    # check if the request was successful
    print "Validate request succeeded:"

    if debug:
        ## for debugging / more information show response:
        print "Validate Request Parameter:"
        print json.dumps(pscrefund.getRequestPrameter(), indent=2)
        print "Validate request Info:"
        print(pscrefund.getRequestInfo())
        print "Validate Refund Response:"
        print json.dumps(pscrefund.getResponse(), indent=2)

    if pscrefund.getResponse()['status'] == 'VALIDATION_SUCCESSFUL':
        print 'Validation was successful.'



        ## validation successful -> execute Refund
        print '###############'
        raw_input("Press Enter to continue to execute refund...")


        ## For usage information have a look at validate Refund above
        # only add refund ID from the prior validation
        pscrefund.executeRefund(payment_id, pscrefund.getResponse()['id'], pscrefund.getResponse()['amount'], pscrefund.getResponse()['currency'], pscrefund.getResponse()['customer']['id'], pscrefund.getResponse()['customer']['email'], customer_ip)

        if pscrefund.requestIsOK():
            # check if the request was successful
            print "Execute Request succeeded:"
            if pscrefund.getResponse()['status'] == 'SUCCESS':
                print 'Refund was successfully executed. Customer has received his refund.'
            else:
                print 'Refund was not successful. Response:'
                print json.dumps(pscrefund.getResponse(), indent=2)
            if debug:
                ## for debugging / more information show response:
                print "Execute Request Parameter:"
                print json.dumps(pscrefund.getRequestPrameter(), indent=2)
                print "Execute Request Info:"
                print(pscrefund.getRequestInfo())
                print "Execute Refund Response:"
                print json.dumps(pscrefund.getResponse(), indent=2)
        else:
            # Refund failed, handle errors
            error = pscrefund.getError()
            print "#### Error ####"
            print "Execute Request failed with Error: " + str(error['number']) + " - "+  error['message']
            if debug:
                print 'Execute debug Response:'
                print json.dumps(pscrefund.getResponse(), indent=2)
                print "###############"

    else:
        # validation not successful
        print 'Validatation not successful. Reponse:'
        print json.dumps(pscrefund.getResponse(), indent=2)

else:
    # payment failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'debug Response:'
        print json.dumps(pscrefund.getResponse(), indent=2)
        print "###############"



## direct Refund
print '###############'
raw_input("Press Enter to continue to direct refund...")

## For usage information have a look above
pscrefund.directRefund(payment_id, amount, currency, customer_id, customer_email, customer_ip)

if pscrefund.requestIsOK():
    # check if the request was successful
    print "Direct refund Request succeeded."
    if pscrefund.getResponse()['status'] == 'SUCCESS':
        print 'Direct Refund was successfully executed. Customer has received his refund.'
    else:
        print 'Direct Refund was not successful. Response:'
        print json.dumps(pscrefund.getResponse(), indent=2)
    if debug:
        ## for debugging / more information show response:
        print "Request Parameter:"
        print json.dumps(pscrefund.getRequestPrameter(), indent=2)
        print "Request Info:"
        print(pscrefund.getRequestInfo())
        print "directly Refund Response:"
        print json.dumps(pscrefund.getResponse(), indent=2)
else:
    #  direct Refund failed, handle errors
    error = pscrefund.getError()
    print "#### Error ####"
    print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'debug Response:'
        print json.dumps(pscrefund.getResponse(), indent=2)
        print "###############"


print '######## Test finished #######'
