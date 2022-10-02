class HttpClientException(Exception):
    def __init__(self, api, response):
        self.method = api.method.name
        self.path = api.path
        self.expected_status = api.expected_status
        self.statusCode = -1
        self.msgDesc = None
        self.messageList = None

        print(response)

        if api is not None and response is not None:
            respJson = response.json()

            self.statusCode = response.status_code
            self.msgDesc = respJson['msgDesc'] if respJson is not None and 'msgDesc' in respJson else None
            self.messageList = respJson['messageList'] if respJson is not None and 'messageList' in respJson else None

        Exception.__init__(self,
                           "{} {} failed: expected_status={}, status={}, message={}".format(self.method, self.path,
                                                                                            self.expected_status,
                                                                                            self.statusCode,
                                                                                            self.msgDesc))
