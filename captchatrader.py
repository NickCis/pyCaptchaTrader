import json
import urllib2
import cookielib
import MultipartPostHandler
from urllib import urlencode

class urldownload:
    def __init__(self, cookies=None):
        self.cookies = cookielib.CookieJar()
        if cookies != None and type(cookies) == type(self.cookies):
            self.cookies = cookies        
        self.proxy = None
        self.auth = None
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies),
                                           MultipartPostHandler.MultipartPostHandler)
    def open(self, url, post=None, get=None ):
        if get:            
            url = "url?%s" % urlencode(get)
        return self.opener.open(url, post, 70)

    def setProxy(self, proxy, auth=None):
        '''proxy, auth
           ip:port, (user,pass)
           xxx.xxx.xxx.xxx:xx'''
        print proxy, auth        
        if proxy == "%s:%s" % (None, None):
            self = urldownload(self.cookies)
            return
        self.proxy = proxy
        self.opener.add_handler(urllib2.ProxyHandler({'http': proxy}))
        if auth:
            self.auth = auth
            proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
            proxy_auth_handler.add_password(None, proxy, auth[0], auth[1])
            self.opener.add_handler(proxy_auth_handler)

class captchatrader:
    def __init__(self, api_key=None):
        if api_key == None:
            print 'Apikey isn\'t setted, only basic functions will be available'
        self.__apikey = api_key
        self.__user = None
        self.__password = None
        self.__download = urldownload()
        self.__lastTicket = None

    def login(self, user, password):
        '''Password could be the passkey'''
        self.__user = user
        self.__password = password

    def submit(self, imagePath, match=None):
        '''Submit a job to be solved. imagePath is the path of the captcha image.
        Returns None if the file can't be opened.'''
        url = "http://api.captchatrader.com/submit"
        try:
            img = open(imagePath, 'rb')
        except IOError as e:
            print e
            return None
        params = {'api_key': self.__apikey,
                  'password': self.__password,
                  'username': self.__user,
                  'value': open(imagePath,'rb')}
        if match != None:
            params.update({'match': match})
        self.__lastTicket, captchastring = self.download(url, params)
        return [self.__lastTicket, captchastring]

    def respond(self, is_correct, ticket=None):
        '''Respond whether or not a job was solved correctly'''
        if ticket == None:
            if self.__lastTicket == None:
                print 'No ticket was passed.'
                return
            ticket = self.__lastTicket
        url = "http://api.captchatrader.com/respond"
        params = {'ticket': ticket,
                  'is_correct': is_correct,
                  'password': self.__password,
                  'username': self.__user}
        self.__lastTicket = None
        return self.download(url, params)

    def getCredits(self):
        '''Get the credits of a user'''
        url = "http://api.captchatrader.com/get_credits/username:%s/password:%s/" % (self.__user, self.__password)
        return self.download(url)

    def enqueue(self):
        '''Request an image to solve'''
        url = "http://api.captchatrader.com/enqueue/username:%s/password:%s/ " % (self.__user, self.__password)
        self.__lastTicket, img = self.download(url)
        return [self.__lastTicket, img]

    def answer(self, value, ticket=None):
        '''Submit an answer to a job'''
        print "ticket: %s, lasticket: %s" % (ticket, self.__lastTicket)
        if ticket == None:
            if self.__lastTicket == None:
                print 'No ticket was passed.'
                return
            ticket = self.__lastTicket
        url = "http://api.captchatrader.com/answer/"
        params = {'ticket': ticket,
                  'value': value,
                  'password': self.__password,
                  'username': self.__user}
        self.__lastTicket = None
        return self.download(url, params)

    def dequeue(self):
        '''Skip a job or remove request from queue'''
        print 'Dequeing'
        self.__lastTicket = None
        url = "http://api.captchatrader.com/answer/"
        params = {'password': self.__password,
                  'username': self.__user}
        return self.download(url, params)

    def getWaitTime(self):
        '''Estimate the remaining wait time'''
        url = "http://api.captchatrader.com/get_wait_time/username:%s/password:%s/" % (self.__user, self.__password)
        return self.download(url)

    def download(self, url, post=None, get=None):
        resp = self.__download.open(url, post, get)
        ret = resp.read()
        resp.close()
        return json.loads(ret)

#if __name__ == "__main__":

