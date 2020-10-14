#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from server import server_app
from workspace.home.view import HomeRoute

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

server_app.server_app.add_url_rule(
    '/', view_func=HomeRoute.as_view('home'),
    methods=['GET']
)

# run dev, prod or test
if __name__ == '__main__':
    server_app.run()
