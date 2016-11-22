# -*- coding: UTF-8 -*-
from __future__ import __package__import absolute_import
from __future__ import __package__import print_function

from pyVim.connect import SmartConnect, Disconnect
import pyVmomi
from pyVmomi import vim

import argparse
import atexit
import getpass
import ssl

try:
    from flask import _app_ctx_stack as _ctx_stack
except ImportError:
    from flask import _request_ctx_stack as _ctx_stack

class Vmomi(object):
    pass
