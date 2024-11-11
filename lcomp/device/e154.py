#! /usr/bin/env python3

"""Константы и функции для работы с модулем E154."""

import logging
from ctypes import POINTER, c_ushort, cast

from numpy import abs, any, array, float32, frombuffer, insert, int16, split, where

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


# диапазон входного напряжения модуля E154
V5000 = 0              # диапазон 5В
V1600 = 64             # диапазон 1.6В
V0500 = 128            # диапазон 0.5В
V0160 = 192            # диапазон 0.16В

# тип синхронизации E154
NO_SYNC = 0             # отсутствие синхронизации ввода
TTL_START_SYNC = 1      # цифровая синхронизация начала ввода
RESERVED_SYNC = 2       # зарезервированное значение для совместимости с другими модулями
ANALOG_SYNC = 3         # аналоговая синхронизация начала ввода

# вид синхронизации E154
A_SYNC_LEVEL = 0        # аналоговая синхронизация по уровню
A_SYNC_EDGE = 1         # аналоговая синхронизация по переходу

# режим синхронизации E154
A_SYNC_UP_EDGE = 0      # по уровню «выше» или переходу «снизу-вверх»
A_SYNC_DOWN_EDGE = 1    # по уровню «ниже» или переходу «сверху-вниз»

# номер канала E154
CH_0 = 0
CH_1 = 1
CH_2 = 2
CH_3 = 3
CH_4 = 4
CH_5 = 5
CH_6 = 6
CH_7 = 7


def GetDataADC(daqpar, descr, address, size):
    """Преобразование кодов АЦП в вольты."""

    GetDataADC.tail = getattr(GetDataADC, "tail", [])

    arr_ptr = cast(address, POINTER(c_ushort * size))[0]

    dataraw = insert(frombuffer(arr_ptr, int16), 0, GetDataADC.tail)
    dataraw, GetDataADC.tail = split(dataraw, [dataraw.size - dataraw.size % daqpar.NCh])
    data12b = dataraw.reshape((daqpar.NCh, -1), order="F") & 0x0FFF
    data12b[data12b > 2048] -= 4096

    if over_chn := where(any(abs(data12b) > 2000, axis=1))[0].tolist():
        _logger.warning("Channels %s overload detected", over_chn)
    data12b = data12b.astype(float32)

    gain = (array(daqpar.Chn) >> 6 & 0x3)[:daqpar.NCh, None]

    VRange = array([5.0, 1.6, 0.5, 0.16], dtype=float32)[gain]

    koef = array(descr.t7.KoefADC, dtype=float32)
    A = koef[gain]              # OffsetCalibration
    B = koef[gain + 4]          # ScaleCalibration

    data12b += A
    data12b *= B
    data12b *= VRange
    data12b /= 2000.0

    return data12b
