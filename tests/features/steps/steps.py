# -*- coding: utf-8 -*-
"""
    Unit        : tests.features.steps
    description : Define the steps of test
    developer   : Alcindo Schleder
    version     : 1.0.0
"""
import os
from behave import given, when, then


@given(u'Renderizar a página principal')
@when(u'Acessa a url raiz')
def get_root_page(context):
    context.page = context.client.get('/')

@then(u'Verifica a página acessada')
def check_root_page(context):
    assert context.page.status_code == 200
