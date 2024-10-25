#! /usr/bin/env python3

"""Константы и функции для работы с модулем E14-440."""

import logging
from ctypes import POINTER, c_ushort, cast

from numpy import (add, array, divide, float32, frombuffer, insert, int16,
                   multiply, split, where)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


# диапазон входного напряжения модуля E440
V10000 = 0              # диапазон 10В
V2500 = 64              # диапазон 2.5В
V0625 = 128             # диапазон 0.625В
V0156 = 192             # диапазон 0.15625В

# тип канала E440
CH_DIFF = 0             # дифференциальный канал
CH_NULL = 16            # калибровка нуля
CH_GRND = 32            # канал с общей землей

# тип синхронизации E440
NO_SYNC = 0             # нет синхронизации
TTL_START_SYNC = 1      # цифровая синхронизация старта, остальные параметры синхронизации не используются
TTL_KADR_SYNC = 2       # по-кадровая синхронизация, остальные параметры синхронизации не используются
ANALOG_SYNC = 3         # аналоговая синхронизация старта по выбранному каналу АЦП

# вид синхронизации E440
A_SYNC_LEVEL = 0        # аналоговая синхронизация по уровню
A_SYNC_EDGE = 1         # аналоговая синхронизация по переходу

# режим синхронизации E440
A_SYNC_UP_EDGE = 0      # по уровню «выше» или переходу «снизу-вверх»
A_SYNC_DOWN_EDGE = 1    # по уровню «ниже» или переходу «сверху-вниз»

# номер канала E440
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
    data14b = where(data14b > 8192, data14b - 16384, data14b)

    overload = (data14b > 8000) | (data14b < -8000)
    if over_chn := [ch for ch in range(overload.shape[0]) if overload[ch].any()]:
        _logger.warning("Channels %s overload detected", over_chn)
    data14b = data14b.astype(float32)

    gain = (array(daqpar.Chn) >> 6 & 0x3)[:daqpar.NCh, None]

    VRange = array([10.0, 2.5, 0.625, 0.15625], dtype=float32)[gain]

    koef = array(descr.t4.KoefADC, dtype=float32)
    A = koef[gain + 0]                          # OffsetCalibration
    B = koef[gain + 4]                          # ScaleCalibration

    add(A, data14b, out=data14b)
    multiply(data14b, B, out=data14b)
    multiply(data14b, VRange, out=data14b)
    divide(data14b, 8000.0, out=data14b)

    return data14b
