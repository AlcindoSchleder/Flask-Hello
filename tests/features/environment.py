# -*- coding: utf-8 -*-
"""
    Unit        : tests.environment
    Description : Define environment configuration to execute the tests
    developer   : Alcindo Schleder
    version     : 1.0.0
"""
import os
import ipdb
from server import server_app as server

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

def before_feature(context, feature):
    # Register all Blueprint
    context.flask = server.server_app
    context.flask.testing = True
    context.flask_context = context.flask.test_request_context()
    context.flask_context.push()
    context.client = context.flask.test_client()


def after_feature(context, feature):
    """
    Actions after testing each feature
    @param context: Context of feature
    @param feature: Current feature
    @return: void
    """


def after_step(context, step):
    """
    Actions to execute on each step of test
    @param context: step context
    @param step: current step
    @return: void
    """
    if step.status == 'failed':
        ipdb.spost_mortem(step.exc_traceback)
