from smtplib import *
from flask import Flask, request, redirect, url_for
app = Flask("NumFOCUS Web App")



# I need to register create a Continuum postmark login and get this
# set up, and then I will give you the API key.  -- pwang
#PostMarkAPIKey = 

numfocus_from_addr = "info@numfocus.org"

HOST = "50.56.188.141"
PORT = 80
MAILGUN_HOST = "smtp.mailgun.org"
MAILGUN_PORT = 587
MAILGUN_LOGIN = "postmaster@continuum.mailgun.org"
MAILGUN_PASSWORD = "5b62r2nv1b79"


@app.route('/mail', methods=["POST"])
def do_mail():
    # request.form is a dict that contains all of the fields of the form
    email_addr = request.form["email"]
    full_name = request.form["full_name"]
    company_name = request.form["company_name"]
    url = request.form["url"]
    comment = request.form["comment"]

    s = SMTP(MAILGUN_HOST, MAILGUN_PORT)

    s.login(MAILGUN_LOGIN, MAILGUN_PASSWORD)

    confirmed_msg = """From: %s
    To: "%s" <%s>
    Subject: NumFOCUS Donorship

    Thank you, your message has been received and someone will respond to you shortly.
    """ % (numfocus_from_addr, full_name, email_addr)

    received_msg = """From: %s
    To: %s
    Subject: New Message Recieved from NumFOCUS Donorship

    A new message has been received:

    Name: %s 
    Email: %s
    URL: %s
    Company: %s

    Message: %s

    """ % (numfocus_from_addr, numfocus_from_addr, full_name, email_adr, url, company_name, comment)

    s.sendmail(numfocus_from_addr, email_addr, msg)
    s.sendmail(numfocus_from_addr, numfocus_from_addr, received_msg)




def tornado_main():
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT, address=HOST)
    IOLoop.instance().start()

if __name__ == "__main__":

    try:
        import tornado
        tornado_main()
    except ImportError:
        app.run(debug=FALSE, host=HOST, port=PORT)


