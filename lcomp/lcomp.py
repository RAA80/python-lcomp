#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import logging
import functools
import platform
from ctypes import (cdll, pointer, byref, c_uint, c_int, c_ushort, c_ulong,
                    c_ulonglong, c_void_p, c_char_p, c_ubyte, POINTER, CFUNCTYPE)
from .ldevioctl import (SLOT_PAR, PLATA_DESCR_U2, DAQ_PAR, ErrorCode,
                        WDAC_PAR_0, WDAC_PAR_1, WADC_PAR_0, WADC_PAR_1)


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def _load_lib(name):
    return cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", name))


if os.name == "posix":
    _wlib = _load_lib("libwlcomp.so")
    _lib = _load_lib("liblcomp.so")
    _hDll = _lib._handle
    _ifc_type = lambda x: pointer(c_void_p(x))
elif os.name == "nt":
    if platform.architecture()[0] == '32bit':
        _wlib = _load_lib("wlcomp.dll")
        _lib = _load_lib("lcomp.dll")
        _hDll = pointer(c_uint(_lib._handle))
    elif platform.architecture()[0] == '64bit':
        _wlib = _load_lib("wlcomp64.dll")
        _lib = _load_lib("lcomp64.dll")
        _hDll = pointer(c_ulonglong(_lib._handle))
    _ifc_type = lambda x: pointer(c_ulong(x))


class IDaqLDevice(c_void_p):
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
        'IoAsync': CFUNCTYPE(c_uint, c_void_p, POINTER(DAQ_PAR)),
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
        'SetParametersStream': CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint, POINTER(c_uint), c_void_p, c_void_p, c_uint),
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
            _logger.error("{} error {} ({})".format(self.name, ret, ErrorCode[ret]))

        return ret

    def __getattr__(self, name):
        self.name = name
        if name in self._functions_:
            return functools.partial(self.__call__, self._functions_[name])


class LCOMP(object):
    data = None         # адрес начала кольцевого буфера
    syncd = None        # переменная синхронизации

    def __init__(self, slot):
        self._hIfc = None
        self._stream_id = None

        self._ldev = IDaqLDevice()
        self.CreateInstance(slot)

    def __enter__(self):
        self.OpenLDevice()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._hIfc:
            self.CloseLDevice()

    def CreateInstance(self, slot):
        ''' Функция создает объект для конкретного слота '''

        err = c_uint(0)

        result = self._ldev.CallCreateInstance(_hDll, slot, byref(err))
        if not result:
            raise Exception("CreateInstance error {} ({})".format(err.value,
                                                        ErrorCode[err.value]))
        self._hIfc = _ifc_type(result)
        return bool(self._hIfc) or None

# Основные функции

    def OpenLDevice(self):
        ''' Функция открывает соответствующий линк драйвера для платы '''

        handle = self._ldev.OpenLDevice(self._hIfc)
        if handle == -1:
            raise Exception("OpenLDevice invalid handle")

        return handle or None

    def CloseLDevice(self):
        ''' Функция для завершения работы с платой '''

        return not self._ldev.CloseLDevice(self._hIfc) or None

    def LoadBios(self, filename):
        ''' Загрузка BIOS в плату.
            В модуль E20-10 загружается прошивка ПЛИС e2010.pld, указывать ее
            нужно также без расширения. У L791 нет загружаемого БИОСа.
            E140 также не требует загрузки БИОС
        '''

        biospath = os.path.join(os.path.dirname(__file__), "bios", filename)
        bios = c_char_p(biospath.encode("ascii"))

        return not self._ldev.LoadBios(self._hIfc, bios) or None

    def PlataTest(self):
        ''' Тест на наличие платы и успешную загрузку.
            Для L791, E14-140 E154 и E20-10 это просто заглушка всегда
            возвращающая успех
        '''

        return not self._ldev.PlataTest(self._hIfc) or None

    def GetSlotParam(self):
        ''' Функция возвращает информацию для указанного виртуального слота '''

        slPar = SLOT_PAR()

        if not self._ldev.GetSlotParam(self._hIfc, byref(slPar)):
            return slPar

    def ReadPlataDescr(self):
        ''' Чтение пользовательского Flash '''

        plDescr = PLATA_DESCR_U2()

        if not self._ldev.ReadPlataDescr(self._hIfc, byref(plDescr)):
            return plDescr

    def WritePlataDescr(self, plDescr, Ena):
        ''' Запись пользовательского Flash '''

        Ena = c_ushort(Ena)

        return not self._ldev.WritePlataDescr(self._hIfc, byref(plDescr), Ena) or None

    def ReadFlashWord(self, address):
        ''' Чтение слова из пользовательского Flash '''

        address = c_ushort(address)
        data = c_ushort(0)

        if not self._ldev.ReadFlashWord(self._hIfc, address, byref(data)):
            return data.value

    def WriteFlashWord(self, address, value):
        ''' Запись слова в пользовательский Flash '''

        address = c_ushort(address)
        value = c_ushort(value)

        return not self._ldev.WriteFlashWord(self._hIfc, address, value) or None

    def RequestBufferStream(self, size, stream_id):
        ''' Выделение памяти под большой кольцевой буфер '''

        size = c_uint(size)
        self._stream_id = stream_id

        if not self._ldev.RequestBufferStream(self._hIfc, byref(size), self._stream_id):
            return size.value

    def FillDAQparameters(self, daqpar):
        ''' Заполняет значениями внутреннюю структуру параметров сбора данных '''

        if isinstance(daqpar, WDAC_PAR_0):   sp_type = c_uint(0)
        elif isinstance(daqpar, WDAC_PAR_1): sp_type = c_uint(1)
        elif isinstance(daqpar, WADC_PAR_0): sp_type = c_uint(2)
        elif isinstance(daqpar, WADC_PAR_1): sp_type = c_uint(3)

        return not self._ldev.FillDAQparameters(self._hIfc, byref(daqpar), sp_type) or None

    def SetParametersStream(self, daqpar, size):
        ''' Настройка платы АЦП/ЦАП на заданные параметры ввода или вывода данных '''

        if isinstance(daqpar, WDAC_PAR_0):   sp_type = c_uint(0)
        elif isinstance(daqpar, WDAC_PAR_1): sp_type = c_uint(1)
        elif isinstance(daqpar, WADC_PAR_0): sp_type = c_uint(2)
        elif isinstance(daqpar, WADC_PAR_1): sp_type = c_uint(3)

        size = c_uint(size)
        data = pointer(c_ushort())
        sync = pointer(c_ulong())

        if not self._ldev.SetParametersStream(self._hIfc, byref(daqpar), sp_type, byref(size), byref(data), byref(sync), self._stream_id):
            self.data = data
            self.syncd = lambda: sync.contents.value

            return True

    def InitStartLDevice(self):
        ''' Инициализация внутренних переменных драйвера перед началом сбора '''

        return not self._ldev.InitStartLDevice(self._hIfc) or None

    def StartLDevice(self):
        ''' Запуск сбора данных с платы в большой кольцевой буфер '''

        return not self._ldev.StartLDevice(self._hIfc) or None

    def StopLDevice(self):
        ''' Остановка сбора данных с платы в большой кольцевой буфер '''

        return not self._ldev.StopLDevice(self._hIfc) or None

    def EnableCorrection(self, Ena):
        ''' Включает/выключает режим коррекции данных '''

        Ena = c_ushort(Ena)

        return not self._ldev.EnableCorrection(self._hIfc, Ena) or None

    def IoAsync(self, daqpar):
        ''' Функция для асинхронных операций ввода/вывода (ввод данных с АЦП,
            вывод данных на ЦАП, работа с цифровыми линиями)
        '''

        return not self._ldev.IoAsync(self._hIfc, byref(daqpar)) or None

    def GetParameter(self, name):
        ''' Функция возвращает некоторые полезные данные о модуле и позволяет
            вместе с SetParameter хранить временно данные пользователя
        '''

        param = c_uint()

        if not self._ldev.GetParameter(self._hIfc, name, byref(param)):
            return param.value

    def SetParameter(self, name, value):
        ''' Функция позволяет хранить временно данные пользователя и получать
            их с помощью GetParameter
        '''

        value = c_uint(value)

        return not self._ldev.SetParameter(self._hIfc, name, byref(value)) or None

    def EnableFlashWrite(self, flag):
        ''' Разрешение записи в пользовательский Flash '''

        flag = c_ushort(flag)

        return not self._ldev.EnableFlashWrite(self._hIfc, flag) or None

    def SendCommand(self, cmd):
        ''' Посылает выбранную команду в DSP '''

        cmd = c_ushort(cmd)

        return not self._ldev.SendCommand(self._hIfc, cmd) or None

    def SetLDeviceEvent(self, event, event_id):
        ''' Установка события в драйвере. Работа события облегчает ожидание
            готовности данных от платы при однократном заполнении буфера
        '''

        event = c_void_p(event)
        event_id = c_uint(event_id)

        return not self._ldev.SetLDeviceEvent(self._hIfc, event, event_id) or None

    def GetWord_DM(self, address):
        ''' Читает слово из памяти данных DSP/модуля '''

        address = c_ushort(address)
        data = c_ushort(0)

        if not self._ldev.GetWord_DM(self._hIfc, address, byref(data)):
            return data.value

    def GetWord_PM(self, address):
        ''' Читает слово из памяти программ DSP/модуля '''

        address = c_ushort(address)
        data = c_uint(0)

        if not self._ldev.GetWord_PM(self._hIfc, address, byref(data)):
            return data.value

    def GetArray_DM(self, address, count):
        ''' Читает массив слов из памяти данных DSP '''

        address = c_ushort(address)
        count = c_uint(count)
        data = c_ushort(0)

        if not self._ldev.GetArray_DM(self._hIfc, address, count, byref(data)):
            result = (c_ushort * count.value)(data)
            return list(result)

    def GetArray_PM(self, address, count):
        ''' Читает массив слов из памяти программ DSP '''

        address = c_ushort(address)
        count = c_uint(count)
        data = c_uint(0)

        if not self._ldev.GetArray_PM(self._hIfc, address, count, byref(data)):
            result = (c_uint * count.value)(data)
            return list(result)

    def PutWord_DM(self, address, data):
        ''' Записывает слово в память данных DSP/модуля '''

        address = c_ushort(address)
        data = c_ushort(data)

        return not self._ldev.PutWord_DM(self._hIfc, address, data) or None

    def PutWord_PM(self, address, data):
        ''' Записывает слово в память программ DSP/модуля '''

        address = c_ushort(address)
        data = c_uint(data)

        return not self._ldev.PutWord_PM(self._hIfc, address, data) or None

    def PutArray_DM(self, address, count, data):
        ''' Записывает массив слов в память данных DSP '''

        address = c_ushort(address)
        data = (c_ushort * count)(*data)
        count = c_uint(count)

        return not self._ldev.PutArray_DM(self._hIfc, address, count, byref(data)) or None

    def PutArray_PM(self, address, count, data):
        ''' Записывает массив слов в память программ DSP '''

        address = c_ushort(address)
        data = (c_uint * count)(*data)
        count = c_uint(count)

        return not self._ldev.PutArray_PM(self._hIfc, address, count, byref(data)) or None

# Функции для работы с портами ввода/вывода плат

    def inbyte(self, offset, length=1, key=0):
        ''' Ввод байта из I/O порта '''

        offset = c_uint(offset)
        data = c_ubyte(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.inbyte(self._hIfc, offset, byref(data), length, key):
            result = (c_ubyte * length.value)(data)
            return list(result)

    def inword(self, offset, length=2, key=0):
        ''' Ввод слова из I/O порта '''

        offset = c_uint(offset)
        data = c_ushort(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.inword(self._hIfc, offset, byref(data), length, key):
            result = (c_ushort * length.value)(data)
            return list(result)

    def indword(self, offset, length=4, key=0):
        ''' Ввод двойного слова из I/O порта '''

        offset = c_uint(offset)
        data = c_uint(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.indword(self._hIfc, offset, byref(data), length, key):
            result = (c_uint * length.value)(data)
            return list(result)

    def inmbyte(self, offset, length=1, key=0):
        ''' Ввод байта из памяти '''

        offset = c_uint(offset)
        data = c_ubyte(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.inmbyte(self._hIfc, offset, byref(data), length, key):
            result = (c_ubyte * length.value)(data)
            return list(result)

    def inmword(self, offset, length=2, key=0):
        ''' Ввод слова из памяти '''

        offset = c_uint(offset)
        data = c_ushort(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.inmword(self._hIfc, offset, byref(data), length, key):
            result = (c_ushort * length.value)(data)
            return list(result)

    def inmdword(self, offset, length=4, key=0):
        ''' Ввод двойного слова из памяти '''

        offset = c_uint(offset)
        data = c_uint(0)
        length = c_uint(length)
        key = c_uint(key)

        if not self._ldev.inmdword(self._hIfc, offset, byref(data), length, key):
            result = (c_uint * length.value)(data)
            return list(result)

    def outbyte(self, offset, data, length=1, key=0):
        ''' Вывод байта в I/O порт '''

        offset = c_uint(offset)
        data = (c_ubyte * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outbyte(self._hIfc, offset, byref(data), length, key) or None

    def outword(self, offset, data, length=2, key=0):
        ''' Вывод слова в I/O порт '''

        offset = c_uint(offset)
        data = (c_ushort * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outword(self._hIfc, offset, byref(data), length, key) or None

    def outdword(self, offset, data, length=4, key=0):
        ''' Вывод двойного слова в I/O порт '''

        offset = c_uint(offset)
        data = (c_uint * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outdword(self._hIfc, offset, byref(data), length, key) or None

    def outmbyte(self, offset, data, length=1, key=0):
        ''' Вывод байта в память '''

        offset = c_uint(offset)
        data = (c_ubyte * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outmbyte(self._hIfc, offset, byref(data), length, key) or None

    def outmword(self, offset, data, length=2, key=0):
        ''' Вывод слова в память '''

        offset = c_uint(offset)
        data = (c_ushort * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outmword(self._hIfc, offset, byref(data), length, key) or None

    def outmdword(self, offset, data, length=4, key=0):
        ''' Вывод двойного слова в память '''

        offset = c_uint(offset)
        data = (c_uint * length)(*data)
        length = c_uint(length)
        key = c_uint(key)

        return not self._ldev.outmdword(self._hIfc, offset, byref(data), length, key) or None


__all__ = [ "LCOMP" ]
