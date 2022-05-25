#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ctypes import cast, POINTER, c_ushort
from numpy import (array, frombuffer, int16, putmask, insert, multiply, divide,
                   float32, split, add)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


V_RESET_DSP_E140       = 0
V_PUT_ARRAY_E140       = 1
V_GET_ARRAY_E140       = 2
V_START_ADC_E140       = 3
V_STOP_ADC_E140        = 4
V_START_ADC_ONCE_E140  = 5
V_START_DAC_E140       = 6
V_STOP_DAC_E140        = 7
V_GET_MODULE_NAME_E140 = 11

L_ADC_PARS_BASE_E140 = 0x0060
L_ADC_ONCE_FLAG_E140 = L_ADC_PARS_BASE_E140 + 136
L_FLASH_ENABLED_E140 = L_ADC_PARS_BASE_E140 + 137
L_DAC_PARS_BASE_E140 = 0x0160

L_TTL_OUT_E140            = 0x0400
L_TTL_IN_E140             = 0x0400
L_ENABLE_TTL_OUT_E140     = 0x0402
L_ADC_SAMPLE_E140         = 0x0410
L_ADC_CHANNEL_SELECT_E140 = 0x0412
L_ADC_START_E140          = 0x0413
L_DAC_SAMPLE_E140         = 0x0420
L_DAC_SAMPLES_E140        = 0x0428
L_SUSPEND_MODE_E140       = 0x0430
L_DATA_FLASH_BASE_E140    = 0x0800
L_CODE_FLASH_BASE_E140    = 0x1000
L_BIOS_VERSION_E140       = 0x1080
L_DESCRIPTOR_BASE_E140    = 0x2780
L_RAM_E140                = 0x8000


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

    gain = (array(daqpar.Chn) >> 6 & 0x3)[:daqpar.NCh, None]

    VRange = array([10.0, 2.5, 0.625, 0.15625], dtype=float32)[gain]

    koef = array(plDescr.t5.KoefADC, dtype=float32)
    A = koef[gain + 0]                          # OffsetCalibration
    B = koef[gain + 4]                          # ScaleCalibration

    add(A, data14b, out=data14b)                #
    multiply(data14b, B, out=data14b)           # Оптимизированная версия ...
    multiply(data14b, VRange, out=data14b)      # ... (A + data14b) * B * VRange / 8000.0
    divide(data14b, 8000.0, out=data14b)        #

    return data14b
