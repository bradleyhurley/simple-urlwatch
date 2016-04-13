import os
import urllib2
import smtplib
from difflib import SequenceMatcher

#SMTP Configuration
smtp_sender = """Sender Email Account"""
receivers = ['FirstEmail', 'Second Email']
smtp_host = """SMTP Host Name"""
smtp_port = 587
smtp_password = 'Sender Email Password'
smtp_subject = 'Simple-URLWatch has detected a change!'


# URLs to monitor
URLS = {
    '1': 'http://espn.com',
    '2': 'http://reddit.com/new',
    '3': 'http://www.google.com'
}


THRESHOLD = 1.0  # on a scale of 0 to 1

BASEDIR = os.getcwd()
HTML_PATH = 'html'


def main():
    notify_sender = False
    # create html dir if it does not exist
    if not os.path.exists(os.path.join(BASEDIR, HTML_PATH)):
        try:
            os.makedirs(os.path.join(BASEDIR, HTML_PATH))
        except Exception as e:
            print("Unable to create html directory at {0}".format(os.path.join(BASEDIR, HTML_PATH)))
            print e

    message = 'Subject: {0}\n\nThe following URLS have changed \n'.format(smtp_subject)

    for urlID, url in URLS.items():
        last_html = urlID + '.html'
        last_html_path = os.path.join(BASEDIR, HTML_PATH, last_html)
        
        html = get_html(url)
        if os.path.exists(last_html_path):
            last_html = open(last_html_path, 'r').read()
            score = get_score(html, last_html)

            if score < THRESHOLD:
                message += url + '\n'
                notify_sender = True

            write_html(html, last_html_path)
        else:
            write_html(html, last_html_path)

    if notify_sender is True:
        send_notification(message)


def send_notification(message):
    print message
    try:
        smtp_obj = smtplib.SMTP(smtp_host, smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(smtp_sender, smtp_password)
        smtp_obj.sendmail(smtp_sender, receivers, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"


def get_score(html, last_html):
    sm = SequenceMatcher(None, html, last_html)
    score = sm.ratio()
    return score


def get_html(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except Exception as e:
        print 'Unable to open URL: ' + url
        print e
        exit(1)


def write_html(html, last_html_path):
    with open(last_html_path, 'wb') as f:
        f.write(html)

if __name__ == '__main__':
    main()