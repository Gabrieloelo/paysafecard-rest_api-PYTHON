import requests
import base64
import json
import datetime

class PSCRefund:

    def __init__(self, key, environment):
        #Construct prefund class.
        self.key = key #define psc key
        self.error = {}
        self.environment = environment
        self.setEnvironment()


    def doRequest(self, parameter, method, headers=None):
        """
        Make an API request and return all needed information
        """

        # define default headers
        header = {'Authorization': 'Basic ' + base64.b64encode(self.key), 'Content-Type': 'application/json'}

        self.requestParameter = parameter
        # add additional header
        if headers is not None:
            for key in headers:
                header[key] = headers[key]
        # method handling
        if method == 'POST':
            r = requests.post(self.url, data=json.dumps(parameter), headers=header)
        elif method == 'GET':
            r = requests.get(self.url, headers=header)

        # asign requested data
        self.request = r
        self.requestinfo = {}
        self.requestinfo['links'] = r.links
        self.requestinfo['status_code'] = r.status_code
        self.requestinfo['reason'] = r.reason
        self.requestinfo['response'] = r.request
        self.requestinfo['url'] = r.url
        self.requestinfo['headers'] = r.headers
        self.requestinfo['apparent_encoding'] =  r.apparent_encoding

        # Reset URL
        self.setEnvironment()


    def requestIsOK(self):
        # check if request was successful
        if self.request.status_code < 300:
            return True
        else:
            return False

    def getResponse(self):
        # get the response
        if not self.request.json():
            return {}
        else:
            return self.request.json()

    def getRequestPrameter(self):
        # get request parameter
        return self.requestParameter

    def getRequestInfo(self):
        # get Request Information
        return self.requestinfo


    def setEnvironment(self):
        # set the environment and URLs
        if self.environment == 'TEST':
            self.url = 'https://apitest.paysafecard.com/v1/payments/'
        elif self.environment == 'PRODUCTION':
            self.url = 'https://api.paysafecard.com/v1/payments/'
        else:
            print "#### environment not supported"

    def getPaymentDetail(self, payment_id):
        # get Payment Details including the (requested) refunds
        self.url = self.url + payment_id
        self.doRequest({}, 'GET')
        # return False if request failed
        if self.requestIsOK:
            return self.getResponse()
        else:
            return False

    def validateRefund(self, payment_id, amount, currency, customer_id, customer_email, customer_ip, correlation_id=None, submerchant_id=None):
        # validate a Refund
        """
        necessary variables:
        payment_id = 'pay_1000005843_U38vg4sGgcVnl2GTWuCp3eumn3j3nHkn_EUR' # the refund's payment ID
        amount = 10.00 # refund amount
        currency = 'EUR' # refund currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_email = 'ABCEXAMPLEABC@ABCEXAMPLEABC.ABC' # customer to refund to
        customer_ip = '123.123.123.123' # the customers IP

        optionla variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}

        customer = {
        'id': customer_id,
        'email': customer_email,
        'first_name': 'Test',
        'last_name': 'Test',
        'date_of_birth': '1990-01-09',
        'ip': customer_ip,
        }

        parameter = {
            'amount' : amount,
            'currency' : currency,
            'type' : 'PAYSAFECARD',
            'customer' : customer,
            'capture' : 'false',
        }

        if submerchant_id is not None:
            parameter['submerchant_id'] = submerchant_id

        if correlation_id is not None:
            headers['Correlation-ID'] = correlation_id

        self.url = self.url + payment_id + '/refunds'
        self.doRequest(parameter, 'POST', headers)

        if self.requestIsOK:
            return self.getResponse()
        else:
            return False


    def executeRefund(self, payment_id, refund_id, amount, currency, customer_id, customer_email, customer_ip, correlation_id=None, submerchant_id=None):
        # execute a validated Refund
        """
        necessary variables:
        payment_id = 'pay_1000005843_U38vg4sGgcVnl2GTWuCp3eumn3j3nHkn_EUR' # the refund's payment ID
        refund_id = 'ref_1000005843_8j6BBuHXOhvWBMKn20uhEEGrRMngwD7g_EUR' # the refund's id (from a prior validation)
        amount = 10.00 # refund amount
        currency = 'EUR' # refund currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_email = 'ABCEXAMPLEABC@ABCEXAMPLEABC.ABC' # customer to refund to
        customer_ip = '123.123.123.123' # the customers IP

        optionla variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}

        customer = {
        'id': customer_id,
        'email': customer_email,
        'first_name': 'Test',
        'last_name': 'Test',
        'date_of_birth': '1990-01-09',
        'ip': customer_ip,
        }

        parameter = {
            'amount' : amount,
            'currency' : currency,
            'type' : 'PAYSAFECARD',
            'customer' : customer,
            'capture' : 'true',
        }

        if submerchant_id is not None:
            parameter['submerchant_id'] = submerchant_id

        if correlation_id is not None:
            headers['Correlation-ID'] = correlation_id

        self.url = self.url + payment_id + '/refunds/' + refund_id + '/capture'
        self.doRequest(parameter, 'POST', headers)


        if self.requestIsOK:
            return self.getResponse()
        else:
            return False



    def directRefund(self, payment_id, amount, currency, customer_id, customer_email, customer_ip, correlation_id=None, submerchant_id=None):
        # directly refund
        """
        necessary variables:
        payment_id = 'pay_1000005843_U38vg4sGgcVnl2GTWuCp3eumn3j3nHkn_EUR' # the refund's payment ID
        amount = 10.00 # refund amount
        currency = 'EUR' # refund currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_email = 'ABCEXAMPLEABC@ABCEXAMPLEABC.ABC' # customer to refund to
        customer_ip = '123.123.123.123' # the customers IP

        optionla variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}

        customer = {
        'id': customer_id,
        'email': customer_email,
        'first_name': 'Test',
        'last_name': 'Test',
        'date_of_birth': '1990-01-09',
        'ip': customer_ip,
        }

        parameter = {
            'amount' : amount,
            'currency' : currency,
            'type' : 'PAYSAFECARD',
            'customer' : customer,
            'capture' : 'true',
        }

        if submerchant_id is not None:
            parameter['submerchant_id'] = submerchant_id

        if correlation_id is not None:
            headers['Correlation-ID'] = correlation_id

        self.url = self.url + payment_id + '/refunds'
        self.doRequest(parameter, 'POST', headers)

        if self.requestIsOK:
            return self.getResponse()
        else:
            return False

    def getError(self):
        # get Errors request errors and returned errors

        if self.request.status_code == 400:
            self.error['number'] = "HTTP:400"
            self.error['message'] = 'Logical error. The requested URL cannot be found. Check your request data'
        elif self.request.status_code == 403:
            self.error['number']  = "HTTP:403"
            self.error['message'] = 'Transaction could not be initiated due to connection problems. The servers IP address is probably not whitelisted!'
        elif self.request.status_code == 500:
            self.error['number']  = "HTTP:500"
            self.error['message'] = 'Server error.'

        if self.error:
            return self.error

        if 'number' in self.getResponse():
            if self.getResponse()['number'] == 3160:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Invalid customer details. Please forward the customer to contact our support'
            elif self.getResponse()['number'] == 3162:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'E-mail address is not registered with mypaysafecard'
            elif self.getResponse()['number'] == 3165:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'The amount is invalid. Maximum refund amount cannot exceed the original payment amount'
            elif self.getResponse()['number'] == 3167:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Customer limit exceeded. Please forward the customer to contact our support'
            elif self.getResponse()['number'] == 3179:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'The amount is invalid. Maximum refund amount cannot exceed the original payment amount'
            elif self.getResponse()['number'] == 3180:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Original Transaction is in an invalid state'
            elif self.getResponse()['number'] == 3181:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Merchantclient-ID is not matching with original transaction'
            elif self.getResponse()['number'] == 3182:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Merchantclient-ID is a mandatory parameter'
            elif self.getResponse()['number'] == 3184:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Original payment transaction does not exist'
            elif self.getResponse()['number'] == 10028:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'One or more neccessary parameters are empty'

        return self.error
