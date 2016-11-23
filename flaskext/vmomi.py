# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import pyVmomi

import argparse
import atexit
import getpass
import ssl

try:
    from flask import _app_ctx_stack as _ctx_stack
except ImportError:
    from flask import _request_ctx_stack as _ctx_stack

class Vmomi(object):
    def __init__(self, app=None, **connect_args):
        self.connect_args = connect_args
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app
        self.app.config.setdefault('VMware_vCenter_HOST', 'localhost')
        self.app.config.setdefault('VMware_vCenter_PORT', 443)
        self.app.config.setdefault('VMware_vCenter_USER', 'Administrator')
        self.app.config.setdefault('VMware_vCenter_PASSWORD', None)
        #Flask 0.9 or later
        if hasattr(app, 'teardown_appcontext'):
            self.app.teardown_request(self.teardown_request)
        #Flask 0.7 to 0.8
        elif hasattr(app, 'teardown_request'):
            self.app.teardown_request(self.teardown_request)
        #Older versions
        else:
            self.app.after_request(self.teardown_request)
    
    def connect(self):
        if self.app.config['VMware_vCenter_HOST']:
            self.connect_args['host'] = self.app.config['VMware_vCenter_HOST']
        if self.app.config['VMware_vCenter_PORT']:
            self.connect_args['port'] = self.app.config['VMware_vCenter_PORT']
        if self.app.config['VMware_vCenter_USER']:
            self.connect_args['user'] = self.app.config['VMware_vCenter_USER']
        if self.app.config['VMware_vCenter_PASSWORD']:
            self.connect_args['password'] = self.app.config['VMware_vCenter_PASSWORD']
        context = None
        if hasattr(ssl, '_create_unverified_context'):
      	    context = ssl._create_unverified_context()
        link = SmartConnect(host=args.host,
                     user=args.user,
                     pwd=password,
                     port=int(args.port),
                     sslContext=context)
        if not link:
            print("Could not connect to the specified host using specified username and password")
       	    return -1
        atexit.register(Disconnect, link)
        return link
  
    def teardown_request(self, exception):
        ctx = _ctx_stack.top
        if hasattr(ctx, "vm_omi"):
            ctx.vm_omi.close()

    def get_db(self):
        ctx = _ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "vm_omi"):
                ctx.vm_omi = self.connect()
            return ctx.vm_omi

