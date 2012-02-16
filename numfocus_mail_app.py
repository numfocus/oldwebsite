# Flask is the python web micro-framework we will use.
# If it doesn't exist on the server, then install it via "easy_install flask"
from flask import Flask, request, redirect, url_for
app = Flask("NumFOCUS Web App")

# This is the HTML text that will be sent out in the email to everyone.
# Maybe we shouldn't use HTML text for these emails, since many of the
# receipients may be on plaintext mail clients?
confirmation_text = """
Thank you for your submission, %s.

Someone will be contacting you shortly.

The NumFOCUS Team.
"""

submission_text = """
The following submission was made at %s
Name: %s 
Email: %s 
Company: %s
URL: %s
Message: %s
"""

# I need to register create a Continuum postmark login and get this
# set up, and then I will give you the API key.  -- pwang
#PostMarkAPIKey = 

numfocus_from_addr = "info@numfocus.org"

HOST = "50.56.188.141"
PORT = 80


@app.route('/mail', methods=["POST"])
def do_mail():
    # request.form is a dict that contains all of the fields of the form
    email_addr = request.form["email"]
    full_name = request.form["full_name"]
    company_name = request.form["company_name"]
    URL = request.form["URL"]
    Comment = request.form["comment"]


    # PostMark is an outbound email service that we will use to send 
    # emails programmatically from things like web apps.
    # This "postmark" module is a simple way to interface with
    # their mail system from Python.  Grab it from:
    #     https://github.com/themartorana/python-postmark
    from postmark import PMMail

    confirm_mailer = PMMail(
                api_key = PostMarkAPIKey,
                sender = numfocus_from_addr,
                to = '"%s" <%s>' % (full_name, email_addr),
                subject = "Welcome to NumFOCUS!",
                html_body = confirmation_text % full_name
    )
    
    confirm_mailer.send(test = False)

    submission_mailer = PMMail(
                api_key = PostMarkAPIKey,
                sender = numfocus_from_addr,
                to = '%s' % info@numfocus.org,
                subject = "New Message Received from Donor Form",
                html_body = submission_text % ("", full_name, email, company_name, URL, comment)
    )
    
    submission_mailer.send(test = False) 




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


