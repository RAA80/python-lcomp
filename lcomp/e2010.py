#! /usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import array, frombuffer, int16, putmask, insert
from ctypes import cast, POINTER, c_ushort
import logging

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


_data14b_tail = []

def GetDataADC(daqpar, plDescr, address, size):
    global _data14b_tail

    arr_ptr = cast(address, POINTER(c_ushort * size))[0]

    data14b = frombuffer(arr_ptr, int16, count=size)
    data14b = insert(data14b, 0, _data14b_tail)
    _data14b_tail = data14b[data14b.size - data14b.size % daqpar.NCh:]
    data14b = data14b[:data14b.size - data14b.size % daqpar.NCh].reshape((daqpar.NCh, -1), order='F') & 0x3FFF

    putmask(data14b, data14b > 8192, data14b - 16384)
    gain = []
    for ch in range(daqpar.NCh):
        if daqpar.Chn[ch] == 0:
            if (daqpar.AdcIMask & (SIG_0 | V03_0)) == (SIG_0 | V03_0):   gain.append(2)
            elif (daqpar.AdcIMask & (SIG_0 | V10_0)) == (SIG_0 | V10_0): gain.append(1)
            elif (daqpar.AdcIMask & (SIG_0 | V30_0)) == (SIG_0 | V30_0): gain.append(0)
            else: gain.append(0)
        elif daqpar.Chn[ch] == 1:
            if (daqpar.AdcIMask & (SIG_1 | V03_1)) == (SIG_1 | V03_1):   gain.append(2)
            elif (daqpar.AdcIMask & (SIG_1 | V10_1)) == (SIG_1 | V10_1): gain.append(1)
            elif (daqpar.AdcIMask & (SIG_1 | V30_1)) == (SIG_1 | V30_1): gain.append(0)
            else: gain.append(0)
        elif daqpar.Chn[ch] == 2:
            if (daqpar.AdcIMask & (SIG_2 | V03_2)) == (SIG_2 | V03_2):   gain.append(2)
            elif (daqpar.AdcIMask & (SIG_2 | V10_2)) == (SIG_2 | V10_2): gain.append(1)
            elif (daqpar.AdcIMask & (SIG_2 | V30_2)) == (SIG_2 | V30_2): gain.append(0)
            else: gain.append(0)
        elif daqpar.Chn[ch] == 3:
            if (daqpar.AdcIMask & (SIG_3 | V03_3)) == (SIG_3 | V03_3):   gain.append(2)
            elif (daqpar.AdcIMask & (SIG_3 | V10_3)) == (SIG_3 | V10_3): gain.append(1)
            elif (daqpar.AdcIMask & (SIG_3 | V30_3)) == (SIG_3 | V30_3): gain.append(0)
            else: gain.append(0)
    gain = array(gain)[:daqpar.NCh, None]

    if data14b[(data14b > 8000) | (data14b < -8000)].any():
        _logger.warning("Channel overload detected !!!")

    VRange = array([3.0, 1.0, 0.3])[gain]

    if plDescr.t6.Rev == "A":
        A = array(plDescr.t6.KoefADC)[gain + 0]           # OffsetCalibration
        B = array(plDescr.t6.KoefADC)[gain + 12]          # ScaleCalibration

        return (A + data14b) * B * VRange / 8000.0
    else:
        return data14b * VRange / 8000.0
