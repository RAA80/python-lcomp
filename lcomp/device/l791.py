#! /usr/bin/env python3

"""Константы и функции для работы с модулем L791."""

import logging
from ctypes import POINTER, c_ushort, cast

from numpy import abs, any, array, float32, frombuffer, insert, int16, split, where

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


# диапазон входного напряжения модуля L791
V10000 = 0              # диапазон 10В
V5000 = 64              # диапазон 5В
V2500 = 128             # диапазон 2.5В
V1250 = 192             # диапазон 1.25В
V0625 = 256             # диапазон 0.625В
V0312 = 320             # диапазон 0.312В
V0156 = 384             # диапазон 0.156В
V0078 = 448             # диапазон 0.078В

# номер канала L791
CH_0 = 0
CH_1 = 1
CH_2 = 2
CH_3 = 3
CH_4 = 4
CH_5 = 5
CH_6 = 6
CH_7 = 7
CH_8 = 8
CH_9 = 9
CH_10 = 10
CH_11 = 11
CH_12 = 12
CH_13 = 13
CH_14 = 14
CH_15 = 15


def GetDataADC(daqpar, descr, address, size):
    """Преобразование кодов АЦП в вольты."""

    GetDataADC.tail = getattr(GetDataADC, "tail", [])

    arr_ptr = cast(address, POINTER(c_ushort * size))[0]

    dataraw = insert(frombuffer(arr_ptr, int16), 0, GetDataADC.tail)
    dataraw, GetDataADC.tail = split(dataraw, [dataraw.size - dataraw.size % daqpar.NCh])
    data14b = dataraw.reshape((daqpar.NCh, -1), order="F") & 0x3FFF
    data14b[data14b > 8192] -= 16384

    if over_chn := where(any(abs(data14b) > 8192, axis=1))[0].tolist():
        _logger.warning("Channels %s overload detected", over_chn)
    data14b = data14b.astype(float32)

    gain = (array(daqpar.Chn) >> 6 & 0x7)[:daqpar.NCh, None]

    VRange = array([10.0, 5.0, 2.5, 1.25, 0.625, 0.312, 0.156, 0.078], dtype=float32)[gain]

    koef = array(descr.t3.KoefADC, dtype=float32)
    A = koef[gain]                              # OffsetCalibration
    B = koef[gain + 8]                          # ScaleCalibration

    data14b += A
    data14b *= B
    data14b *= VRange
    data14b /= 8192.0

    return data14b
