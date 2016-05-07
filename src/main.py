import os

import jinja2
import webapp2

from google.appengine.api import mail, app_identity
from models import Player


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = Player.query()
        for user in users:
            if user.latest_game().state in (0, 1):
                subject = 'This is a reminder!'
                body = 'Hello {}, try out Guess A Number!'.format(user.name)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA2.get_template('index.html')
        self.response.write(template.render())


JINJA2 = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/client"),
    # loader=jinja2.FileSystemLoader('client'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


APP = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/crons/send_reminder', SendReminderEmail),
], debug=True)
