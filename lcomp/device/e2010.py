#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ctypes import cast, POINTER, c_ushort
from numpy import (array, frombuffer, int16, insert, multiply, divide, float32,
                   split, add, where)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


# E2010 bit macros for channel input range and mode config, use |/+ operator to configure
V30_0 = 0x0000      # диапазон 3В для 0 канала
V10_0 = 0x0008      # диапазон 1В для 0 канала
V03_0 = 0x0010      # диапазон 0.3В для 0 канала
GND_0 = 0x0000      # вход заземлен для 0 канала
SIG_0 = 0x0400      # вход подключен к сигналу для 0 канала

V30_1 = 0x0000      # диапазон 3В для 1 канала
V10_1 = 0x0002      # диапазон 1В для 1 канала
V03_1 = 0x0004      # диапазон 0.3В для 1 канала
GND_1 = 0x0000      # вход заземлен для 1 канала
SIG_1 = 0x0200      # вход подключен к сигналу для 1 канала

V30_2 = 0x0000      # диапазон 3В для 2 канала
V10_2 = 0x8000      # диапазон 1В для 2 канала
V03_2 = 0x0100      # диапазон 0.3В для 2 канала
GND_2 = 0x0000      # вход заземлен для 2 канала
SIG_2 = 0x1000      # вход подключен к сигналу для 2 канала

V30_3 = 0x0000      # диапазон 3В для 3 канала
V10_3 = 0x2000      # диапазон 1В для 3 канала
V03_3 = 0x4000      # диапазон 0.3В для 3 канала
GND_3 = 0x0000      # вход заземлен для 3 канала
SIG_3 = 0x0800      # вход подключен к сигналу для 3 канала

# тип синхронизации E2010
INT_START_TRANS     = 0x01      # внутренний старт с разрешением трансляции сигнала на разъем
INT_START           = 0x81      # просто внутренний старт
EXT_START_UP        = 0x84      # внешний импульс старта по переднему фронту
EXT_START_DOWN      = 0x94      # внешний импульс старта по заднему фронту
EXT_START_DOWN_REVB = 0x8C      # внешний импульс старта по заднему фронту для ревизии B

# источник тактовых импульсов для АЦП E2010
INT_CLK_TRANS = 0x00            # внутренний источник с трансляцией
INT_CLK       = 0x40            # просто внутренний источник
EXT_CLK_UP    = 0x42            # внешний источник, по переднему фронту
EXT_CLK_DOWN  = 0x62            # внешний источник, по заднему фронту

# режим аналоговой синхронизации и номер канала E2010
A_SYNC_OFF       = 0x0000       # нет аналоговой синхронизации
A_SYNC_UP_EDGE   = 0x0080       # синхронизация по переднему фронту
A_SYNC_DOWN_EDGE = 0x0084       # синхронизация по заднему фронту
A_SYNC_HL_LEVEL  = 0x0088       # синхронизация по положительному уровню
A_SYNC_LH_LEVEL  = 0x008C       # синхронизация по отрицательно уровню

# номер канала E2010
CH_0 = 0x00
CH_1 = 0x01
CH_2 = 0x02
CH_3 = 0x03


def _gain_index(mask, channel):
    return {CH_0: {bool(mask & SIG_0 and mask & V03_0): 2,
                   bool(mask & SIG_0 and mask & V10_0): 1},
            CH_1: {bool(mask & SIG_1 and mask & V03_1): 2,
                   bool(mask & SIG_1 and mask & V10_1): 1},
            CH_2: {bool(mask & SIG_2 and mask & V03_2): 2,
                   bool(mask & SIG_2 and mask & V10_2): 1},
            CH_3: {bool(mask & SIG_3 and mask & V03_3): 2,
                   bool(mask & SIG_3 and mask & V10_3): 1}
           }[channel].get(True, 0)


def GetDataADC(daqpar, descr, address, size):
    ''' Чтение данных из буфера. Преобразование кодов АЦП в вольты '''

    GetDataADC.tail = getattr(GetDataADC, "tail", [])

    arr_ptr = cast(address, POINTER(c_ushort * size))[0]

    dataraw = insert(frombuffer(arr_ptr, int16), 0, GetDataADC.tail)
    dataraw, GetDataADC.tail = split(dataraw, [dataraw.size - dataraw.size % daqpar.NCh])
    data14b = dataraw.reshape((daqpar.NCh, -1), order='F') & 0x3FFF
    data14b = where(data14b > 8192, data14b - 16384, data14b)

    overload = (data14b > 8000) | (data14b < -8000)
    over_chn = [ch for ch in range(overload.shape[0]) if overload[ch].any()]
    if over_chn:
        _logger.warning("Channels %s overload detected !!!", over_chn)
    data14b = data14b.astype(float32)

    gain = array([_gain_index(daqpar.AdcIMask, daqpar.Chn[ch])
                  for ch in range(daqpar.NCh)])[:daqpar.NCh, None]
    VRange = array([3.0, 1.0, 0.3], dtype=float32)[gain]

    if descr.t6.Rev == "A":
        koef = array(descr.t6.KoefADC, dtype=float32)
        A = koef[gain + 0]                          # OffsetCalibration
        B = koef[gain + 12]                         # ScaleCalibration

        add(A, data14b, out=data14b)
        multiply(data14b, B, out=data14b)

    multiply(data14b, VRange, out=data14b)
    divide(data14b, 8000.0, out=data14b)

    return data14b
