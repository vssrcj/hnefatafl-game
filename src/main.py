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
            if user.latest_game().state == 0:
                message = mail.EmailMessage(
                    sender='noreply@{}.appspotmail.com'.format(app_id),
                    subject='Hnefatafl reminder'
                    )
                message.to = user.email
                message.html = """
                    Hello {}, <br/><br/> You are still playing a game in
                    Hnefatafl. <br/>Head over to
                    <a href="https://hnefatafl-game.appspot.com">
                    hnefatafl-game.appspot.com</a>
                    to play some more!
                """.format(user.name)
                message.send()


CRON = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
], debug=False)
