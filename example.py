import captchatrader
APIKEY = ''
if __name__ == '__main__':
    print 'Enter username'
    user = raw_input('user:')
    print 'Enter password'
    password = raw_input('password:')
    if APIKEY == '':
        print 'Apikey wasn\'t configured. If needed please edit de APIKEY= part. Entering your apikey'
        ct = captchatrader.captchatrader()
    else:
        ct = captchatrader.captchatrader(APIKEY)
    ct.login(user, password)
    loop = True
    while loop:
        print 'What do you want to do?'
        print '1) Submit'
        print '2) Respond'
        print '3) Get Credits'
        print '4) Enqueue'
        print '5) Answer'
        print '6) Dequeue'
        print '7) Get Wait Time'
        print '8) Exit'
        action = raw_input('Action number:')
        if int(action) == 1:
            var = raw_input('Enter the path of the image')
            print 'Submiting. Please wait...'
            print ct.submit(var)
        elif int(action) == 2:
            var = raw_input('Tiket id:')
            var2 = raw_input('Was it correct? y/n')
            if var2.lower() == 'n':
                var2 = False
            else:
                var2 = True
            print 'Responding. Plase wait...'
            print ct.submit(var, var2)
        elif int(action) == 3:
            print 'Getting credits. Please wait...'
            cred = ct.getCredits()
            print cred
            print "Available credits: %s" % cred[1]
        elif int(action) == 4:
            print 'Entering to the queue. Please wait...'
            print ct.enqueue()
        elif int(action) == 5:
            var = raw_input('Tiket id:')
            var2 = raw_input('Answer to the captcha:')
            print 'Submiting. Please wait...'
            print ct.answer(var, var2)
        elif int(action) == 6:
            print 'Getting out of the queue and disconecting. Please wait...'
            print ct.dequeue()
        elif int(action) == 7:
            print 'Getting wait time. Please Wait...'
            var = ct.getWaitTime()
            print var
            print 'You have to wait %s seconds' % var[2]
        elif int(action) == 8:
            print 'Exiting. Please wait...'
            ct.dequeue()
            loop = False
    exit()
