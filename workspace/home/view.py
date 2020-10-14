# -*- coding: utf-8 -*-
from flask import render_template
from flask.views import View
from server import server_app as server

APP_BASE_NAME = 'home'

class HomeRoute(View):
    """
        class       : HomeRoute
        description : Root Route of Application
        developer   : Alcindo Schleder
        version     : 1.0.0
        test version: 1
        test status : passed
    """

    template_name = None

    def dispatch_request(self):
        data = {'user': 'Alcindo Schleder'}
        self.template_name = f'{APP_BASE_NAME}/index.html'
        return render_template(self.template_name, data=data), 200

