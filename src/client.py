""" Expose the default '/' endpoint, and returns the index.html
for the web application """

import os

import jinja2
import webapp2


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
    ('/', MainPage)
], debug=True)
