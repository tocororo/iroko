# -*- coding: utf-8; -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""OAI harvester signals."""

from blinker import Namespace

_signals = Namespace()

harvest_finished = _signals.signal('harvest-finished')
"""
This signal is sent when a harvest has completed.

Example subscriber

.. code-block:: python

    def listener(sender, records, *args, **kwargs):
        for record in records:
            pass
"""
