# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class BankingsystemConfig(AppConfig):
    name = 'SecureBank'

    def ready(self):
        import SecureBank.signals
