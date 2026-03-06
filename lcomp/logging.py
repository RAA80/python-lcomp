#! /usr/bin/env python3

"""Вывод логирующего сообщения вместо вызова исключения."""

import inspect
import logging

from lcomp.lcomp import LCOMP, LcompError

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def decorator(func):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LcompError as err:
            _logger.error("%s error (%s)", func.__name__, err)
    return wraper


for name, func in inspect.getmembers(LCOMP, inspect.isfunction):
    if name not in {"__init__", "__enter__", "__exit__", "CreateInstance",
                    "OpenLDevice", "Get_LDEV2_Interface"}:
        setattr(LCOMP, name, decorator(func))
