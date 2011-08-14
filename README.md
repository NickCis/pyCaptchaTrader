captchatrader
=============

Python bindings for the captchatrader.com API. Submit captcha images, retrieve the text as a string, receive captcha image and submit its result.


Features
--------

* Submit capture images and retrieve the text
* Notify server if text is correct to prevent charging credits on incorrectly detected captchas
* Retrieve amount of credits left
* Get captcha image
* Submit the result of the captcha image getted

Usage
--------

    # Import captchatrader
    import captchatrader
    
    # Initialize (apikey is optional)
    captcha = captchatrader.captchatrader({apikey}) # where {apikey} is your apikey

    # Submit a capture image to retrieve the text
    answer = captcha.submit({imagepath}) # where {imagepath} is a absolute path to the image
    print 'Captcha answer: %s" % answer[1]

    # Tell the server that this captcha has been detected incorrectly (prevent charging credits)
    # An optional argument 'ticket' might be passed, this will override the use of the last ticket
    captcha.respond(False)
  
    # Credits left for this username
    credits = captcha.getCredits()
    print 'Your Credits are: %s' % credits[1]

Requirements
------------

* None (only pyGtk & pygtkwebkit for gui examples)

License
-------

MultipartPostHandler has its own licence (see the file for further details) by Will Holcomb <wholcomb@gmail.com>

The rest: Gnu gpl v 3

Copyright (c) 2011 NickCis

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

