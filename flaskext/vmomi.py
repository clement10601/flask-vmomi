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
        self.app.config.setdefault('VMWARE_VC_HOST', '127.0.0.1')
        self.app.config.setdefault('VMWARE_VC_PORT', 443)
        self.app.config.setdefault('VMWARE_VC_USER', 'admin')
        self.app.config.setdefault('VMWARE_VC_PASSWORD', 'admin')
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
        if self.app.config['VMWARE_VC_HOST']:
            self.connect_args['host'] = self.app.config['VMWARE_VC_HOST']
        if self.app.config['VMWARE_VC_PORT']:
            self.connect_args['port'] = self.app.config['VMWARE_VC_PORT']
        if self.app.config['VMWARE_VC_USER']:
            self.connect_args['user'] = self.app.config['VMWARE_VC_USER']
        if self.app.config['VMWARE_VC_PASSWORD']:
            self.connect_args['pwd'] = self.app.config['VMWARE_VC_PASSWORD']
        context = None
        if hasattr(ssl, '_create_unverified_context'):
      	    context = ssl._create_unverified_context()

        """
        link = SmartConnect(host=self.connect_args['host'],
                     user=self.connect_args['user'],
                     pwd=self.connect_args['password'],
                     port=int(self.connect_args['port']),
                     sslContext=context)
        """

        link = SmartConnect(sslContext=context ,**self.connect_args)
        if not link:
            print("[Error] Could not connect to the specified host using specified username and password")
       	    return -1
        else:
            print("[Info] vCenter Connection Successfully established")
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

