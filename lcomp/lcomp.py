#! /usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging
import os
import platform
from ctypes import (CFUNCTYPE, POINTER, byref, c_char_p, c_int, c_ubyte, c_uint,
                    c_ulonglong, c_ushort, c_void_p, cast, cdll, pointer)

from .ldevioctl import (ERROR_CODE, PLATA_DESCR_U2, SLOT_PAR, WADC_PAR_0,
                        WADC_PAR_1, WASYNC_PAR, WDAC_PAR_0, WDAC_PAR_1)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def _load_lib(name):
    return cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", name))


if os.name == "posix":
    _wlib = _load_lib("libwlcomp.so")
    _lib = _load_lib("liblcomp.so")
    _hdll = _lib._handle
    _ifc_type = lambda x: c_void_p(x)
elif os.name == "nt":
    if platform.architecture()[0] == '32bit':
        _wlib = _load_lib("wlcomp.dll")
        _lib = _load_lib("lcomp.dll")
        _hdll = pointer(c_uint(_lib._handle))
        _ifc_type = lambda x: pointer(c_uint(x))
    elif platform.architecture()[0] == '64bit':
        _wlib = _load_lib("wlcomp64.dll")
        _lib = _load_lib("lcomp64.dll")
        _hdll = pointer(c_ulonglong(_lib._handle))
        _ifc_type = lambda x: pointer(c_ulonglong(x))


class IDaqLDevice(c_void_p):
    ''' Основной интерфейс для работы с устройствами '''

    _functions_ = {         # arg1 - return value, arg2 - interface pointer, arg3+ - func arguments
        'CallCreateInstance': CFUNCTYPE(c_void_p, c_void_p, c_uint, POINTER(c_uint)),

        'CloseLDevice': CFUNCTYPE(c_uint, c_void_p),
        'EnableCorrection': CFUNCTYPE(c_uint, c_void_p, c_ushort),
        'EnableFlashWrite': CFUNCTYPE(c_uint, c_void_p, c_ushort),
        'FillDAQparameters': CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint),
        'GetArray_DM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_ushort)),
        'GetArray_PM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_uint)),
        'GetParameter': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint)),
        'GetSlotParam': CFUNCTYPE(c_uint, c_void_p, POINTER(SLOT_PAR)),
        'GetWord_DM': CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_ushort)),
        'GetWord_PM': CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_uint)),
        'inbyte': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        'indword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        'InitStartLDevice': CFUNCTYPE(c_uint, c_void_p),
        'inmbyte': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        'inmdword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        'inmword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        'inword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        'IoAsync': CFUNCTYPE(c_uint, c_void_p, POINTER(WASYNC_PAR)),
        'LoadBios': CFUNCTYPE(c_uint, c_void_p, c_char_p),
        'OpenLDevice': CFUNCTYPE(c_int, c_void_p),
        'outbyte': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        'outdword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        'outmbyte': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        'outmdword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        'outmword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        'outword': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        'PlataTest': CFUNCTYPE(c_uint, c_void_p),
        'PutArray_DM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_ushort)),
        'PutArray_PM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_uint)),
        'PutWord_DM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_ushort),
        'PutWord_PM': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint),
        'ReadFlashWord': CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_ushort)),
        'ReadPlataDescr': CFUNCTYPE(c_uint, c_void_p, POINTER(PLATA_DESCR_U2)),
        'RequestBufferStream': CFUNCTYPE(c_uint, c_void_p, POINTER(c_uint), c_uint),
        'SendCommand': CFUNCTYPE(c_uint, c_void_p, c_ushort),
        'SetLDeviceEvent': CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint),
        'SetParameter': CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint)),
        'SetParametersStream': CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint, POINTER(c_uint), POINTER(c_void_p), POINTER(c_void_p), c_uint),
        'StartLDevice': CFUNCTYPE(c_uint, c_void_p),
        'StopLDevice': CFUNCTYPE(c_uint, c_void_p),
        'WriteFlashWord': CFUNCTYPE(c_uint, c_void_p, c_ushort, c_ushort),
        'WritePlataDescr': CFUNCTYPE(c_uint, c_void_p, POINTER(PLATA_DESCR_U2), c_ushort),
    }

    def __call__(self, *args):
        prototype = args[0]
        arguments = args[1:]

        ret = prototype((self.name, _wlib))(*arguments)
        if ret and self.name not in ("CallCreateInstance", "OpenLDevice"):
            _logger.error("%s error %d (%s)", self.name, ret, ERROR_CODE[ret])

        return ret

    def __getattr__(self, name):
        self.name = name
        if name in self._functions_:
            return functools.partial(self.__call__, self._functions_[name])


class LCOMP(object):
    ''' Python wrapper for lcomp library '''

    def __init__(self, slot):
        self._ifc = None
        self._stream_id = None

        self._ldev = IDaqLDevice()
        self.CreateInstance(slot)

    def __enter__(self):
        if self.OpenLDevice():
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._ifc:
            self.CloseLDevice()

    def CreateInstance(self, slot):
        ''' Функция создает объект для конкретного слота '''

        err = c_uint()

        result = self._ldev.CallCreateInstance(_hdll, c_uint(slot), byref(err))
        if not result:
            raise Exception("CreateInstance error {} ({})".format(err.value,
                                                       ERROR_CODE[err.value]))
        self._ifc = _ifc_type(result)
        return bool(self._ifc) or None

# Основные функции

    def OpenLDevice(self):
        ''' Функция открывает соответствующий линк драйвера для платы '''

        if self._ldev.OpenLDevice(self._ifc) == -1:
            raise Exception("OpenLDevice invalid handle")

        return True

    def CloseLDevice(self):
        ''' Функция для завершения работы с платой '''

        return not self._ldev.CloseLDevice(self._ifc) or None

    def LoadBios(self, filename):
        ''' Загрузка BIOS в плату.
            В модуль E20-10 загружается прошивка ПЛИС e2010.pld, указывать ее
            нужно также без расширения. У L791 нет загружаемого БИОСа.
            E140 также не требует загрузки БИОС
        '''

        biospath = os.path.join(os.path.dirname(__file__), "bios", filename)
        bios = c_char_p(biospath.encode("ascii"))

        return not self._ldev.LoadBios(self._ifc, bios) or None

    def PlataTest(self):
        ''' Тест на наличие платы и успешную загрузку.
            Для L791, E14-140 E154 и E20-10 это просто заглушка всегда
            возвращающая успех
        '''

        return not self._ldev.PlataTest(self._ifc) or None

    def GetSlotParam(self):
        ''' Функция возвращает информацию для указанного виртуального слота '''

        sl_par = SLOT_PAR()

        if not self._ldev.GetSlotParam(self._ifc, byref(sl_par)):
            return sl_par

    def ReadPlataDescr(self):
        ''' Чтение пользовательского Flash '''

        descr = PLATA_DESCR_U2()

        if not self._ldev.ReadPlataDescr(self._ifc, byref(descr)):
            return descr

    def WritePlataDescr(self, descr, ena):
        ''' Запись пользовательского Flash '''

        return not self._ldev.WritePlataDescr(self._ifc, byref(descr),
                                              c_ushort(ena)) or None

    def ReadFlashWord(self, address):
        ''' Чтение слова из пользовательского Flash '''

        data = c_ushort()

        if not self._ldev.ReadFlashWord(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def WriteFlashWord(self, address, value):
        ''' Запись слова в пользовательский Flash '''

        return not self._ldev.WriteFlashWord(self._ifc, c_ushort(address),
                                             c_ushort(value)) or None

    def RequestBufferStream(self, size, stream_id):
        ''' Выделение памяти под большой кольцевой буфер '''

        size = c_uint(size)
        self._stream_id = c_uint(stream_id)

        if not self._ldev.RequestBufferStream(self._ifc, byref(size), self._stream_id):
            return size.value

    def FillDAQparameters(self, daqpar):
        ''' Заполняет значениями внутреннюю структуру параметров сбора данных '''

        sp_type = {WDAC_PAR_0: c_uint(0),
                   WDAC_PAR_1: c_uint(1),
                   WADC_PAR_0: c_uint(2),
                   WADC_PAR_1: c_uint(3),
                  }[type(daqpar)]

        return not self._ldev.FillDAQparameters(self._ifc, byref(daqpar),
                                                sp_type) or None

    def SetParametersStream(self, daqpar, size):
        ''' Настройка платы АЦП/ЦАП на заданные параметры ввода или вывода данных '''

        sp_type = {WDAC_PAR_0: c_uint(0),
                   WDAC_PAR_1: c_uint(1),
                   WADC_PAR_0: c_uint(2),
                   WADC_PAR_1: c_uint(3),
                  }[type(daqpar)]

        data = pointer(c_void_p())
        sync = pointer(c_void_p())

        if not self._ldev.SetParametersStream(self._ifc, byref(daqpar),
                                              sp_type, byref(c_uint(size)),
                                              data, sync, self._stream_id):
            data = cast(data.contents.value, POINTER(c_ushort))
            sync = cast(sync.contents.value, POINTER(c_uint))

            return data, lambda: sync.contents.value

    def InitStartLDevice(self):
        ''' Инициализация внутренних переменных драйвера перед началом сбора '''

        return not self._ldev.InitStartLDevice(self._ifc) or None

    def StartLDevice(self):
        ''' Запуск сбора данных с платы в большой кольцевой буфер '''

        return not self._ldev.StartLDevice(self._ifc) or None

    def StopLDevice(self):
        ''' Остановка сбора данных с платы в большой кольцевой буфер '''

        return not self._ldev.StopLDevice(self._ifc) or None

    def EnableCorrection(self, ena):
        ''' Включает/выключает режим коррекции данных '''

        return not self._ldev.EnableCorrection(self._ifc, c_ushort(ena)) or None

    def IoAsync(self, daqpar):
        ''' Функция для асинхронных операций ввода/вывода (ввод данных с АЦП,
            вывод данных на ЦАП, работа с цифровыми линиями)
        '''

        return not self._ldev.IoAsync(self._ifc, byref(daqpar)) or None

    def GetParameter(self, name):
        ''' Функция возвращает некоторые полезные данные о модуле и позволяет
            вместе с SetParameter хранить временно данные пользователя
        '''

        param = c_uint()

        if not self._ldev.GetParameter(self._ifc, c_uint(name), byref(param)):
            return param.value

    def SetParameter(self, name, value):
        ''' Функция позволяет хранить временно данные пользователя и получать
            их с помощью GetParameter
        '''

        return not self._ldev.SetParameter(self._ifc, c_uint(name),
                                           byref(c_uint(value))) or None

    def EnableFlashWrite(self, flag):
        ''' Разрешение записи в пользовательский Flash '''

        return not self._ldev.EnableFlashWrite(self._ifc, c_ushort(flag)) or None

    def SendCommand(self, cmd):
        ''' Посылает выбранную команду в DSP '''

        return not self._ldev.SendCommand(self._ifc, c_ushort(cmd)) or None

    def SetLDeviceEvent(self, event, event_id):
        ''' Установка события в драйвере. Работа события облегчает ожидание
            готовности данных от платы при однократном заполнении буфера
        '''

        return not self._ldev.SetLDeviceEvent(self._ifc, c_void_p(event),
                                              c_uint(event_id)) or None

    def GetWord_DM(self, address):
        ''' Читает слово из памяти данных DSP/модуля '''

        data = c_ushort()

        if not self._ldev.GetWord_DM(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def GetWord_PM(self, address):
        ''' Читает слово из памяти программ DSP/модуля '''

        data = c_uint()

        if not self._ldev.GetWord_PM(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def GetArray_DM(self, address, count):
        ''' Читает массив слов из памяти данных DSP '''

        data = pointer(c_ushort())

        if not self._ldev.GetArray_DM(self._ifc, c_ushort(address),
                                      c_uint(count), data):
            return data[:count]

    def GetArray_PM(self, address, count):
        ''' Читает массив слов из памяти программ DSP '''

        data = pointer(c_uint())

        if not self._ldev.GetArray_PM(self._ifc, c_ushort(address),
                                      c_uint(count), data):
            return data[:count]

    def PutWord_DM(self, address, data):
        ''' Записывает слово в память данных DSP/модуля '''

        return not self._ldev.PutWord_DM(self._ifc, c_ushort(address),
                                         c_ushort(data)) or None

    def PutWord_PM(self, address, data):
        ''' Записывает слово в память программ DSP/модуля '''

        return not self._ldev.PutWord_PM(self._ifc, c_ushort(address),
                                         c_uint(data)) or None

    def PutArray_DM(self, address, count, data):
        ''' Записывает массив слов в память данных DSP '''

        return not self._ldev.PutArray_DM(self._ifc, c_ushort(address), c_uint(count),
                                          (c_ushort * count)(*data)) or None

    def PutArray_PM(self, address, count, data):
        ''' Записывает массив слов в память программ DSP '''

        return not self._ldev.PutArray_PM(self._ifc, c_ushort(address), c_uint(count),
                                          (c_uint * count)(*data)) or None

# Функции для работы с портами ввода/вывода плат

    def inbyte(self, offset, length=1, key=0):
        ''' Ввод байта из I/O порта '''

        data = c_ubyte()

        if not self._ldev.inbyte(self._ifc, c_uint(offset), byref(data),
                                 c_uint(length), c_uint(key)):
            return data.value

    def inword(self, offset, length=2, key=0):
        ''' Ввод слова из I/O порта '''

        data = c_ushort()

        if not self._ldev.inword(self._ifc, c_uint(offset), byref(data),
                                 c_uint(length), c_uint(key)):
            return data.value

    def indword(self, offset, length=4, key=0):
        ''' Ввод двойного слова из I/O порта '''

        data = c_uint()

        if not self._ldev.indword(self._ifc, c_uint(offset), byref(data),
                                  c_uint(length), c_uint(key)):
            return data.value

    def inmbyte(self, offset, length=1, key=0):
        ''' Ввод байта из памяти '''

        data = c_ubyte()

        if not self._ldev.inmbyte(self._ifc, c_uint(offset), byref(data),
                                  c_uint(length), c_uint(key)):
            return data.value

    def inmword(self, offset, length=2, key=0):
        ''' Ввод слова из памяти '''

        data = c_ushort()

        if not self._ldev.inmword(self._ifc, c_uint(offset), byref(data),
                                  c_uint(length), c_uint(key)):
            return data.value

    def inmdword(self, offset, length=4, key=0):
        ''' Ввод двойного слова из памяти '''

        data = c_uint()

        if not self._ldev.inmdword(self._ifc, c_uint(offset), byref(data),
                                   c_uint(length), c_uint(key)):
            return data.value

    def outbyte(self, offset, data, length=1, key=0):
        ''' Вывод байта в I/O порт '''

        return not self._ldev.outbyte(self._ifc, c_uint(offset),
                                      byref(c_ubyte(data)),
                                      c_uint(length), c_uint(key)) or None

    def outword(self, offset, data, length=2, key=0):
        ''' Вывод слова в I/O порт '''

        return not self._ldev.outword(self._ifc, c_uint(offset),
                                      byref(c_ushort(data)),
                                      c_uint(length), c_uint(key)) or None

    def outdword(self, offset, data, length=4, key=0):
        ''' Вывод двойного слова в I/O порт '''

        return not self._ldev.outdword(self._ifc, c_uint(offset),
                                       byref(c_uint(data)),
                                       c_uint(length), c_uint(key)) or None

    def outmbyte(self, offset, data, length=1, key=0):
        ''' Вывод байта в память '''

        return not self._ldev.outmbyte(self._ifc, c_uint(offset),
                                       byref(c_ubyte(data)),
                                       c_uint(length), c_uint(key)) or None

    def outmword(self, offset, data, length=2, key=0):
        ''' Вывод слова в память '''

        return not self._ldev.outmword(self._ifc, c_uint(offset),
                                       byref(c_ushort(data)),
                                       c_uint(length), c_uint(key)) or None

    def outmdword(self, offset, data, length=4, key=0):
        ''' Вывод двойного слова в память '''

        return not self._ldev.outmdword(self._ifc, c_uint(offset),
                                        byref(c_uint(data)),
                                        c_uint(length), c_uint(key)) or None


__all__ = [ "LCOMP" ]
