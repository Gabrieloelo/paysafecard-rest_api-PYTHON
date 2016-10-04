import requests
import base64
import json
import datetime

class PSCPayout:

    def __init__(self, key, environment):
        #Construct payout class.
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
            self.url = 'https://apitest.paysafecard.com/v1/payouts/'
        elif self.environment == 'PRODUCTION':
            self.url = 'https://api.paysafecard.com/v1/payouts/'
        else:
            print "#### environment not supported"

    def getPayoutDetail(self, payment_id):
        # get payout Details
        self.url = self.url + payment_id
        self.doRequest({}, 'GET')
        # return False if request failed
        if self.requestIsOK:
            return self.getResponse()
        else:
            return False

    def getLimits(self, currency):
        # get Limits
        self.url = self.url + 'limits/' + currency
        self.doRequest({}, 'GET')
        # return False if request failed
        if self.requestIsOK:
            return self.getResponse()
        else:
            return False

    def validatePayout(self, amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday, correlation_id=None, submerchant_id=None):
        # validate a payout
        """
        necessary variables:
        amount = 10.00 # payout amount
        currency = 'EUR' # payout currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_email = 'ABCEXAMPLEABC@ABCEXAMPLEABC.ABC'
        customer_ip = '123.123.123.123' # the customers IP
        first_name = 'John' #  first name
        last_name = 'Doe' #  last name
        birthday = '1986-06-16' # day of birth

        optionla variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}

        customer = {
        'id': customer_id,
        'email': customer_email,
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': birthday,
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

        self.doRequest(parameter, 'POST', headers)

        if self.requestIsOK:
            return self.getResponse()
        else:
            return False


    def executePayout(self, amount, currency, customer_id, customer_email, customer_ip, first_name, last_name, birthday, correlation_id=None, submerchant_id=None):
        # execute a payout
        """
        necessary variables:
        amount = 10.00 # payout amount
        currency = 'EUR' # payoutt currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_email = 'ABCEXAMPLEABC@ABCEXAMPLEABC.ABC'
        customer_ip = '123.123.123.123' # the customers IP
        first_name = 'John' #  first name
        last_name = 'Doe' #  first name
        last_name = 'Doe' #  first name
        birthday = '1986-06-16' # day of birth

        optionla variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}

        customer = {
        'id': customer_id,
        'email': customer_email,
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': birthday,
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
            if self.getResponse()['number'] == 3162:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Unfortunately, no my paysafecard account exists under the e-mail address you have entered. Please check the address for a typing error. If you do not have a my paysafecard account, you can register for one online now for free.'
            elif self.getResponse()['number'] == 3195:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'The personal details associated with your my paysafecard account do not match the details of this account. Please check the first names, surnames and dates of birth entered in both accounts and request the payout again.'
            elif self.getResponse()['number'] == 3234:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Unfortunately, the payout could not be completed due to a problem which has arisen with your my paysafecard account. paysafecard has already sent you an e-mail with further information on this. Please follow the instructions found in this e-mail before requesting the payout again.'
            elif self.getResponse()['number'] == 3198:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Unfortunately, the payout could not be completed due to a problem which has arisen with your my paysafecard account. Please contact the paysafecard support team. info@paysafecard.com'
            elif self.getResponse()['number'] == 10008:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Invalid API Key'
            else:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Unfortunately there has been a technical problem and your payout request could not be executed. If the problem persists, please contact our customer support: support@company.com';

        return self.error
