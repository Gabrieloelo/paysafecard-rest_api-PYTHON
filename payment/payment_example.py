from PSCPayment import PSCPayment
import socket
import uuid
import json # for proper dumping


#debug
debug = False

# your psc key
key = 'psc_xl0EwfLX-96bEkjy-mXYD7SFviyvaqA'

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


## optional features for advanced usage
#
## Define a unique identifier for referencing (optional) default is None
# default: None
# max length: 41
#correlation_id = str(uuid.uuid4())
#correlation_id = 'uniq_id_123'
#
## restrict to certain country
# default: None
#country_restriction = 'DE'
#
## only allow customers with a certain kyc level
# default: None
#kyc_restriction = 'FULL'
#
## set the minimum age of the customer
# default: None
#min_age = 18
#
## chose the shop id to use for this payment
# default: None
#shop_id = 1
#
## Reporting Criteria
# default: None
#submerchant_id = 1
#
# Usage:
#pscpayment.createPayment(amount, currency, customer_id, customer_ip, success_url, failure_url, notification_url, correlation_id, country_restriction, kyc_restriction, min_age, shop_id, submerchant_id)
#
# create a payment
pscpayment.createPayment(amount , currency, customer_id, customer_ip, success_url, failure_url, notification_url)

if pscpayment.requestIsOK():
    # check if the createpayment request was successful

    print 'Request succeeded:'
    print '###############'
    print 'Redirect to (for testing open in browser): ' + pscpayment.getResponse()['redirect']['auth_url']
    if debug:
        ## for debugging / more information show response:
        print "Request Parameter:"
        print json.dumps(pscpayment.getRequestPrameter(), indent=2)
        print "Request Info:"
        print(pscpayment.getRequestInfo())
        print "Request Response:"
        print json.dumps(pscpayment.getResponse(), indent=2)

    ## Retrieve Payment information
    in_payment_id = raw_input("Please enter Payment ID from URL: ")
    # retieve all information
    print '###############'
    print "Retrieve Payment:"
    pscpayment.retrievePayment(in_payment_id)


    if pscpayment.requestIsOK(): # check if last request was successful

        print 'retrive payment successful.'
        if debug:
            print json.dumps(pscpayment.getResponse(), indent=2)

        ## Test for capturing a payment (use in notification script, use in success script as fallback if notification fails. Use when status is AUTHORIZED)
        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            # payment was not captured properly by notification URL
            # Run test if everything works:
            print 'Payment was not captured by notification URL'
            raw_input("Press Enter to continue to capture payment...")
            print "Captured Payment:"
            pscpayment.capturePayment(in_payment_id)

            # check if capture request was successful
            if pscpayment.requestIsOK():
                # capture was successful
                print 'Capture request was successful. Checking response:'
                if debug:
                    print json.dumps(pscpayment.getResponse(), indent=2)

                if pscpayment.getResponse()['status'] == 'SUCCESS':
                    print 'capture successful, process your payment actions'
                    """
                     *                Payment OK
                     *        Here you can save the Payment
                     * process your actions here (i.e. send confirmation email etc.)
                     *  This is a fallback to notification
                     *
                    """
                else:
                    print 'capture not successful, check response:'
                    print json.dumps(pscpayment.getResponse(), indent=2)

            else:
                # capture failed
                error = pscpayment.getError()
                print "#### Error ####"
                print "# Request failed with Error: " + str(error['number']) + " - "+  error['message']
                if debug:
                    print 'Debug information:'
                    print json.dumps(pscpayment.getResponse(), indent=2)
                    print '###############'

        elif  pscpayment.getResponse()['status'] == 'SUCCESS':
            # retrieved payment has success status
            # print a positive response to the customer
            print 'payment status success - Thank you for your purchase!'
            if debug:
                print 'Retrieve Reponse'
                print json.dumps(pscpayment.getResponse(), indent=2)

        elif  pscpayment.getResponse()['status'] == 'INITIATED':
            # payment is iniated but not yet payed / failed
            print 'paymenmt is not yet processed, please visit / redirect to auth_url your received on payment creation'
            print 'exit.'



    else:
        # retrive payment failed, handle errors
        error = pscpayment.getError()
        print "#### Error ####"
        print "Request failed with Error: " + str(error['number']) + " - "+  error['message']
        if debug:
            print 'Debug information:'
            print json.dumps(pscpayment.getResponse(), indent=2)
            print '###############'

else:
    # create payment failed, handle errors
    error = pscpayment.getError()
    print "#### Error ####"
    print "Request failed with Error: " + str(error['number']) + " - "+  error['message']
    if debug:
        print 'Debug information:'
        print json.dumps(pscpayment.getResponse(), indent=2)
        print '###############'
