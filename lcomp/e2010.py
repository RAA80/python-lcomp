#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ctypes import cast, POINTER, c_ushort, LittleEndianStructure, Union, c_uint16
from numpy import (array, frombuffer, int16, putmask, insert, multiply, divide,
                   float32, split, add)

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
INT_START_TRANS     = 0x01          # внутренний старт с разрешением трансляции сигнала на разъем
INT_START           = 0x81          # просто внутренний старт
EXT_START_UP        = 0x84          # внешний импульс старта по переднему фронту
EXT_START_DOWN      = 0x94          # внешний импульс старта по заднему фронту
EXT_START_DOWN_REVB = 0x8C          # внешний импульс старта по заднему фронту для ревизии B

# источник тактовых импульсов для АЦП E2010
INT_CLK_TRANS = 0x00                # внутренний источник с трансляцией
INT_CLK       = 0x40                # просто внутренний источник
EXT_CLK_UP    = 0x42                # внешний источник, по переднему фронту
EXT_CLK_DOWN  = 0x62                # внешний источник, по заднему фронту

# режим аналоговой синхронизации и номер канала E2010
A_SYNC_OFF       = 0x0000           # нет аналоговой синхронизации
A_SYNC_UP_EDGE   = 0x0080           # синхронизация по переднему фронту
A_SYNC_DOWN_EDGE = 0x0084           # синхронизация по заднему фронту
A_SYNC_HL_LEVEL  = 0x0088           # синхронизация по положительному уровню
A_SYNC_LH_LEVEL  = 0x008C           # синхронизация по отрицательно уровню

# номер канала E2010
CH_0 = 0x00
CH_1 = 0x01
CH_2 = 0x02
CH_3 = 0x03


class _AdcIMask_bits(LittleEndianStructure):
    _fields_ = [("_",     c_uint16, 1),
                ("V10_1", c_uint16, 1),
                ("V03_1", c_uint16, 1),
                ("V10_0", c_uint16, 1),
                ("V03_0", c_uint16, 1),
                ("_",     c_uint16, 3),
                ("V03_2", c_uint16, 1),
                ("SIG_1", c_uint16, 1),
                ("SIG_0", c_uint16, 1),
                ("SIG_3", c_uint16, 1),
                ("SIG_2", c_uint16, 1),
                ("V10_3", c_uint16, 1),
                ("V03_3", c_uint16, 1),
                ("V10_2", c_uint16, 1)]

class _AdcIMask(Union):
    _anonymous_ = ("bit",)
    _fields_ = [("bit", _AdcIMask_bits),
                ("value", c_uint16)]

def _gain_index(mask, channel):
    if channel == 0:
        if mask.SIG_0 & mask.V03_0: return 2
        elif mask.SIG_0 & mask.V10_0: return 1
        elif mask.SIG_0: return 0
        else: return 0
    elif channel == 1:
        if mask.SIG_1 & mask.V03_1: return 2
        elif mask.SIG_1 & mask.V10_1: return 1
        elif mask.SIG_1: return 0
        else: return 0
    elif channel == 2:
        if mask.SIG_2 & mask.V03_2: return 2
        elif mask.SIG_2 & mask.V10_2: return 1
        elif mask.SIG_2: return 0
        else: return 0
    elif channel == 3:
        if mask.SIG_3 & mask.V03_3: return 2
        elif mask.SIG_3 & mask.V10_3: return 1
        elif mask.SIG_3: return 0
        else: return 0

def GetDataADC(daqpar, plDescr, address, size):
    GetDataADC.tail = getattr(GetDataADC, "tail", [])

    arr_ptr = cast(address, POINTER(c_ushort * size))[0]

    dataraw = insert(frombuffer(arr_ptr, int16), 0, GetDataADC.tail)
    dataraw, GetDataADC.tail = split(dataraw, [dataraw.size - dataraw.size % daqpar.NCh,])
    data14b = dataraw.reshape((daqpar.NCh, -1), order='F') & 0x3FFF
    putmask(data14b, data14b > 8192, data14b - 16384)

    if data14b[(data14b > 8000) | (data14b < -8000)].any():
        _logger.warning("Channel overload detected !!!")
    data14b = data14b.astype(float32)

    mask = _AdcIMask()
    mask.value = daqpar.AdcIMask
    gain = array([_gain_index(mask, daqpar.Chn[ch]) for ch in range(daqpar.NCh)])[:daqpar.NCh, None]

    VRange = array([3.0, 1.0, 0.3], dtype=float32)[gain]

    if plDescr.t6.Rev == "A":
        koef = array(plDescr.t6.KoefADC, dtype=float32)
        A = koef[gain + 0]                          # OffsetCalibration
        B = koef[gain + 12]                         # ScaleCalibration

        add(A, data14b, out=data14b)                #
        multiply(data14b, B, out=data14b)           # Оптимизированная версия ...
        multiply(data14b, VRange, out=data14b)      # ... (A + data14b) * B * VRange / 8000.0
        divide(data14b, 8000.0, out=data14b)        #
    else:
        multiply(data14b, VRange, out=data14b)      # Оптимизированная версия ...
        divide(data14b, 8000.0, out=data14b)        # ... data14b * VRange / 8000.0

    return data14b
