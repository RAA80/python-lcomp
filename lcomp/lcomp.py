#! /usr/bin/env python3

"""Реализация класса для управления АЦП/ЦАП фирмы LCARD."""

from __future__ import annotations

import logging
import os
import platform
from ctypes import (CDLL, CFUNCTYPE, POINTER, byref, c_char_p, c_int, c_ubyte,
                    c_uint, c_ulonglong, c_ushort, c_void_p, cast, cdll, pointer)
from functools import partial

from .ioctl import (L_ERROR, L_EVENT, L_STREAM, PLATA_DESCR_U2, SLOT_PAR, WADC_PAR_0,
                    WADC_PAR_1, WASYNC_PAR, WDAC_PAR_0, WDAC_PAR_1, WDAQ_PAR)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def _load_lib(name: str) -> CDLL:
    return cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", name))


if os.name == "posix":
    _wlib = _load_lib("libwlcomp.so")
    _lib = _load_lib("liblcomp.so")
    _hdll = _lib._handle
    _ifc_type = lambda x: c_void_p(x)
elif os.name == "nt":
    if platform.architecture()[0] == "32bit":
        _wlib = _load_lib("wlcomp.dll")
        _lib = _load_lib("lcomp.dll")
        _hdll = pointer(c_uint(_lib._handle))
        _ifc_type = lambda x: pointer(c_uint(x))
    elif platform.architecture()[0] == "64bit":
        _wlib = _load_lib("wlcomp64.dll")
        _lib = _load_lib("lcomp64.dll")
        _hdll = pointer(c_ulonglong(_lib._handle))
        _ifc_type = lambda x: pointer(c_ulonglong(x))


class LcompError(Exception):
    pass


class IDaqLDevice(c_void_p):
    """Основной интерфейс для работы с устройствами."""

    _functions_ = {         # arg1 - return value, arg2 - interface pointer, arg3+ - func arguments
        "CallCreateInstance": CFUNCTYPE(c_void_p, c_void_p, c_uint, POINTER(c_uint)),

        "CloseLDevice": CFUNCTYPE(c_uint, c_void_p),
        "EnableCorrection": CFUNCTYPE(c_uint, c_void_p, c_ushort),
        "EnableFlashWrite": CFUNCTYPE(c_uint, c_void_p, c_ushort),
        "FillDAQparameters": CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint),
        "GetArray_DM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_ushort)),
        "GetArray_PM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_uint)),
        "GetParameter": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint)),
        "GetSlotParam": CFUNCTYPE(c_uint, c_void_p, POINTER(SLOT_PAR)),
        "GetWord_DM": CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_ushort)),
        "GetWord_PM": CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_uint)),
        "inbyte": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        "indword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        "InitStartLDevice": CFUNCTYPE(c_uint, c_void_p),
        "inmbyte": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        "inmdword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        "inmword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        "inword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        "IoAsync": CFUNCTYPE(c_uint, c_void_p, POINTER(WASYNC_PAR)),
        "LoadBios": CFUNCTYPE(c_uint, c_void_p, c_char_p),
        "OpenLDevice": CFUNCTYPE(c_int, c_void_p),
        "outbyte": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        "outdword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        "outmbyte": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ubyte), c_uint, c_uint),
        "outmdword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint), c_uint, c_uint),
        "outmword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        "outword": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_ushort), c_uint, c_uint),
        "PlataTest": CFUNCTYPE(c_uint, c_void_p),
        "PutArray_DM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_ushort)),
        "PutArray_PM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint, POINTER(c_uint)),
        "PutWord_DM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_ushort),
        "PutWord_PM": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_uint),
        "ReadFlashWord": CFUNCTYPE(c_uint, c_void_p, c_ushort, POINTER(c_ushort)),
        "ReadPlataDescr": CFUNCTYPE(c_uint, c_void_p, POINTER(PLATA_DESCR_U2)),
        "RequestBufferStream": CFUNCTYPE(c_uint, c_void_p, POINTER(c_uint), c_uint),
        "SendCommand": CFUNCTYPE(c_uint, c_void_p, c_ushort),
        "SetLDeviceEvent": CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint),
        "SetParameter": CFUNCTYPE(c_uint, c_void_p, c_uint, POINTER(c_uint)),
        "SetParametersStream": CFUNCTYPE(c_uint, c_void_p, c_void_p, c_uint, POINTER(c_uint), POINTER(c_void_p), POINTER(c_void_p), c_uint),
        "StartLDevice": CFUNCTYPE(c_uint, c_void_p),
        "StopLDevice": CFUNCTYPE(c_uint, c_void_p),
        "WriteFlashWord": CFUNCTYPE(c_uint, c_void_p, c_ushort, c_ushort),
        "WritePlataDescr": CFUNCTYPE(c_uint, c_void_p, POINTER(PLATA_DESCR_U2), c_ushort),

        "Get_LDEV2_Interface": CFUNCTYPE(c_void_p, c_void_p, POINTER(c_uint)),
        "InitStartLDeviceEx": CFUNCTYPE(c_uint, c_void_p, c_uint),
        "Release_LDEV2_Interface": CFUNCTYPE(c_uint, c_void_p),
        "StartLDeviceEx": CFUNCTYPE(c_uint, c_void_p, c_uint),
        "StopLDeviceEx": CFUNCTYPE(c_uint, c_void_p, c_uint),
    }

    def __call__(self, prototype, *arguments: tuple) -> int | None:
        result = prototype((self.name, _wlib))(*arguments)

        special_names = {"CallCreateInstance", "OpenLDevice", "Get_LDEV2_Interface"}
        if result and self.name not in special_names:
            msg = f"{self.name} error {result} ({L_ERROR(result).name})"
            _logger.error(msg)

        return result if self.name in special_names else not result or None

    def __getattr__(self, name: str) -> partial:
        self.name = name
        return partial(self.__call__, self._functions_[name])


class LCOMP:
    """Python wrapper for lcomp library."""

    def __init__(self, slot: int) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self._ifc = None
        self._ifc2 = None
        self._stream_id = None
        self._sp_type = {WDAC_PAR_0: c_uint(0),
                         WDAC_PAR_1: c_uint(1),
                         WADC_PAR_0: c_uint(2),
                         WADC_PAR_1: c_uint(3)}

        self._ldev = IDaqLDevice()
        self.CreateInstance(slot)

    def __enter__(self) -> LCOMP:
        """Входной блок контекстного менеджера."""

        if self.OpenLDevice():
            return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Выходной блок контекстного менеджера."""

        if self._ifc:
            self.CloseLDevice()

    def CreateInstance(self, slot: int) -> bool:
        """Функция создает объект для конкретного слота."""

        err = c_uint()

        result = self._ldev.CallCreateInstance(_hdll, c_uint(slot), byref(err))
        if not result:
            msg = f"CreateInstance error {err.value} ({L_ERROR(err.value).name})"
            raise LcompError(msg)

        self._ifc = _ifc_type(result)
        return True

# Основные функции

    def OpenLDevice(self) -> bool:
        """Функция открывает соответствующий линк драйвера для платы."""

        if self._ldev.OpenLDevice(self._ifc) == -1:
            msg = "OpenLDevice invalid handle"
            raise LcompError(msg)

        return True

    def CloseLDevice(self) -> bool:
        """Функция для завершения работы с платой."""

        return self._ldev.CloseLDevice(self._ifc)

    def LoadBios(self, filename: str) -> bool:
        """Загрузка BIOS в плату. В модуль E20-10 загружается прошивка ПЛИС
        e2010.pld, указывать ее нужно также без расширения. У L791 нет
        загружаемого БИОСа. E140 также не требует загрузки БИОС.
        """

        biospath = os.path.join(os.path.dirname(__file__), "bios", filename)
        bios = c_char_p(biospath.encode("ascii"))

        return self._ldev.LoadBios(self._ifc, bios)

    def PlataTest(self) -> bool:
        """Тест на наличие платы и успешную загрузку. Для L791, E14-140 E154 и
        E20-10 это просто заглушка всегда возвращающая успех.
        """

        return self._ldev.PlataTest(self._ifc)

    def GetSlotParam(self) -> SLOT_PAR:
        """Функция возвращает информацию для указанного виртуального слота."""

        sl_par = SLOT_PAR()

        if self._ldev.GetSlotParam(self._ifc, byref(sl_par)):
            return sl_par

    def ReadPlataDescr(self) -> PLATA_DESCR_U2:
        """Чтение пользовательского Flash."""

        descr = PLATA_DESCR_U2()

        if self._ldev.ReadPlataDescr(self._ifc, byref(descr)):
            return descr

    def WritePlataDescr(self, descr: PLATA_DESCR_U2, enable: bool) -> bool:
        """Запись пользовательского Flash."""

        return self._ldev.WritePlataDescr(self._ifc, byref(descr), c_ushort(enable))

    def ReadFlashWord(self, address: int) -> int:
        """Чтение слова из пользовательского Flash."""

        data = c_ushort()

        if self._ldev.ReadFlashWord(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def WriteFlashWord(self, address: int, value: int) -> bool:
        """Запись слова в пользовательский Flash."""

        return self._ldev.WriteFlashWord(self._ifc, c_ushort(address), c_ushort(value))

    def RequestBufferStream(self, size: int, stream_id: L_STREAM) -> int:
        """Выделение памяти под большой кольцевой буфер."""

        size = c_uint(size)
        self._stream_id = c_uint(stream_id)

        if self._ldev.RequestBufferStream(self._ifc, byref(size), self._stream_id):
            return size.value

    def FillDAQparameters(self, daqpar: WDAQ_PAR) -> bool:
        """Заполняет значениями внутреннюю структуру параметров сбора данных."""

        return self._ldev.FillDAQparameters(self._ifc, byref(daqpar),
                                            self._sp_type[type(daqpar)])

    def SetParametersStream(self, daqpar: WDAQ_PAR, size: int) -> tuple:
        """Настройка платы АЦП/ЦАП на заданные параметры ввода или вывода данных."""

        data = pointer(c_void_p())
        sync = pointer(c_void_p())

        if self._ldev.SetParametersStream(self._ifc, byref(daqpar),
                                          self._sp_type[type(daqpar)],
                                          byref(c_uint(size)), data, sync,
                                          self._stream_id):
            data = cast(data.contents.value, POINTER(c_ushort))
            sync = cast(sync.contents.value, POINTER(c_uint))

            return data, lambda: sync.contents.value

    def InitStartLDevice(self) -> bool:
        """Инициализация внутренних переменных драйвера перед началом сбора."""

        return self._ldev.InitStartLDevice(self._ifc)

    def StartLDevice(self) -> bool:
        """Запуск сбора данных с платы в большой кольцевой буфер."""

        return self._ldev.StartLDevice(self._ifc)

    def StopLDevice(self) -> bool:
        """Остановка сбора данных с платы в большой кольцевой буфер."""

        return self._ldev.StopLDevice(self._ifc)

    def EnableCorrection(self, enable: bool) -> bool:
        """Включает/выключает режим коррекции данных."""

        return self._ldev.EnableCorrection(self._ifc, c_ushort(enable))

    def IoAsync(self, daqpar: WASYNC_PAR) -> bool:
        """Функция для асинхронных операций ввода/вывода (ввод данных с АЦП,
        вывод данных на ЦАП, работа с цифровыми линиями).
        """

        return self._ldev.IoAsync(self._ifc, byref(daqpar))

    def GetParameter(self, address: int) -> int:
        """Функция возвращает некоторые полезные данные о модуле и позволяет
        вместе с SetParameter хранить временно данные пользователя.
        """

        param = c_uint()

        if self._ldev.GetParameter(self._ifc, c_uint(address), byref(param)):
            return param.value

    def SetParameter(self, address: int, value: int) -> bool:
        """Функция позволяет хранить временно данные пользователя и получать
        их с помощью GetParameter.
        """

        return self._ldev.SetParameter(self._ifc, c_uint(address), byref(c_uint(value)))

    def EnableFlashWrite(self, flag: bool) -> bool:
        """Разрешение записи в пользовательский Flash."""

        return self._ldev.EnableFlashWrite(self._ifc, c_ushort(flag))

    def SendCommand(self, cmd: int) -> bool:
        """Посылает выбранную команду в DSP."""

        return self._ldev.SendCommand(self._ifc, c_ushort(cmd))

    def SetLDeviceEvent(self, event: int, event_id: L_EVENT) -> bool:
        """Установка события в драйвере. Работа события облегчает ожидание
        готовности данных от платы при однократном заполнении буфера.
        """

        return self._ldev.SetLDeviceEvent(self._ifc, c_void_p(event), c_uint(event_id))

    def GetWord_DM(self, address: int) -> int:
        """Читает слово из памяти данных DSP/модуля."""

        data = c_ushort()

        if self._ldev.GetWord_DM(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def GetWord_PM(self, address: int) -> int:
        """Читает слово из памяти программ DSP/модуля."""

        data = c_uint()

        if self._ldev.GetWord_PM(self._ifc, c_ushort(address), byref(data)):
            return data.value

    def GetArray_DM(self, address: int, count: int) -> tuple[int]:
        """Читает массив слов из памяти данных DSP."""

        data = pointer(c_ushort())

        if self._ldev.GetArray_DM(self._ifc, c_ushort(address), c_uint(count), data):
            return tuple(data[:count])

    def GetArray_PM(self, address: int, count: int) -> tuple[int]:
        """Читает массив слов из памяти программ DSP."""

        data = pointer(c_uint())

        if self._ldev.GetArray_PM(self._ifc, c_ushort(address), c_uint(count), data):
            return tuple(data[:count])

    def PutWord_DM(self, address: int, data: int) -> int:
        """Записывает слово в память данных DSP/модуля."""

        return self._ldev.PutWord_DM(self._ifc, c_ushort(address), c_ushort(data))

    def PutWord_PM(self, address: int, data: int) -> int:
        """Записывает слово в память программ DSP/модуля."""

        return self._ldev.PutWord_PM(self._ifc, c_ushort(address), c_uint(data))

    def PutArray_DM(self, address: int, count: int, data: tuple[int]) -> bool:
        """Записывает массив слов в память данных DSP."""

        return self._ldev.PutArray_DM(self._ifc, c_ushort(address), c_uint(count),
                                      (c_ushort * count)(*data))

    def PutArray_PM(self, address: int, count: int, data: tuple[int]) -> bool:
        """Записывает массив слов в память программ DSP."""

        return self._ldev.PutArray_PM(self._ifc, c_ushort(address), c_uint(count),
                                      (c_uint * count)(*data))

# Функции для работы с портами ввода/вывода плат

    def inbyte(self, offset: int, length: int = 1, key: int = 0) -> int:
        """Ввод байта из I/O порта."""

        data = c_ubyte()

        if self._ldev.inbyte(self._ifc, c_uint(offset), byref(data),
                             c_uint(length), c_uint(key)):
            return data.value

    def inword(self, offset: int, length: int = 2, key: int = 0) -> int:
        """Ввод слова из I/O порта."""

        data = c_ushort()

        if self._ldev.inword(self._ifc, c_uint(offset), byref(data),
                             c_uint(length), c_uint(key)):
            return data.value

    def indword(self, offset: int, length: int = 4, key: int = 0) -> int:
        """Ввод двойного слова из I/O порта."""

        data = c_uint()

        if self._ldev.indword(self._ifc, c_uint(offset), byref(data),
                              c_uint(length), c_uint(key)):
            return data.value

    def inmbyte(self, offset: int, length: int = 1, key: int = 0) -> int:
        """Ввод байта из памяти."""

        data = c_ubyte()

        if self._ldev.inmbyte(self._ifc, c_uint(offset), byref(data),
                              c_uint(length), c_uint(key)):
            return data.value

    def inmword(self, offset: int, length: int = 2, key: int = 0) -> int:
        """Ввод слова из памяти."""

        data = c_ushort()

        if self._ldev.inmword(self._ifc, c_uint(offset), byref(data),
                              c_uint(length), c_uint(key)):
            return data.value

    def inmdword(self, offset: int, length: int = 4, key: int = 0) -> int:
        """Ввод двойного слова из памяти."""

        data = c_uint()

        if self._ldev.inmdword(self._ifc, c_uint(offset), byref(data),
                               c_uint(length), c_uint(key)):
            return data.value

    def outbyte(self, offset: int, data: int, length: int = 1, key: int = 0) -> bool:
        """Вывод байта в I/O порт."""

        return self._ldev.outbyte(self._ifc, c_uint(offset), byref(c_ubyte(data)),
                                  c_uint(length), c_uint(key))

    def outword(self, offset: int, data: int, length: int = 2, key: int = 0) -> bool:
        """Вывод слова в I/O порт."""

        return self._ldev.outword(self._ifc, c_uint(offset), byref(c_ushort(data)),
                                  c_uint(length), c_uint(key))

    def outdword(self, offset: int, data: int, length: int = 4, key: int = 0) -> bool:
        """Вывод двойного слова в I/O порт."""

        return self._ldev.outdword(self._ifc, c_uint(offset), byref(c_uint(data)),
                                   c_uint(length), c_uint(key))

    def outmbyte(self, offset: int, data: int, length: int = 1, key: int = 0) -> bool:
        """Вывод байта в память."""

        return self._ldev.outmbyte(self._ifc, c_uint(offset), byref(c_ubyte(data)),
                                   c_uint(length), c_uint(key))

    def outmword(self, offset: int, data: int, length: int = 2, key: int = 0) -> bool:
        """Вывод слова в память."""

        return self._ldev.outmword(self._ifc, c_uint(offset), byref(c_ushort(data)),
                                   c_uint(length), c_uint(key))

    def outmdword(self, offset: int, data: int, length: int = 4, key: int = 0) -> bool:
        """Вывод двойного слова в память."""

        return self._ldev.outmdword(self._ifc, c_uint(offset), byref(c_uint(data)),
                                    c_uint(length), c_uint(key))

# Расширенный интерфейс для работы с устройствами

    def Get_LDEV2_Interface(self) -> bool:
        """Создать расширенный интерфейс."""

        err = c_uint()

        result = self._ldev.Get_LDEV2_Interface(self._ifc, byref(err))
        if not result:
            msg = f"Get_LDEV2_Interface error {err.value} ({L_ERROR(err.value).name})"
            _logger.error(msg)
            return None

        self._ifc2 = _ifc_type(result)
        return True

    def Release_LDEV2_Interface(self) -> bool:
        """Закрыть расширенный интерфейс."""

        return self._ldev.Release_LDEV2_Interface(self._ifc2)

    def InitStartLDeviceEx(self, stream_id: L_STREAM) -> bool:
        """Функция инициализирует внутренние переменные драйвера перед началом сбора."""

        return self._ldev.InitStartLDeviceEx(self._ifc2, c_uint(stream_id))

    def StartLDeviceEx(self, stream_id: L_STREAM) -> bool:
        """Функция запускает сбор данных с платы в большой кольцевой буфер."""

        return self._ldev.StartLDeviceEx(self._ifc2, c_uint(stream_id))

    def StopLDeviceEx(self, stream_id: L_STREAM) -> bool:
        """Функция останавливает сбор данных с платы в большой кольцевой буфер."""

        return self._ldev.StopLDeviceEx(self._ifc2, c_uint(stream_id))


__all__ = ["LCOMP"]
