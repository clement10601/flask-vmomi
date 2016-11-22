# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import pyvmomi

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

