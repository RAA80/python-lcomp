#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import (Structure, Union, c_uint, c_char, c_ushort, c_float, c_int,
                    c_ubyte, c_double)


# Определения типов плат/модулей. Используется в поле BoardType структуры SLOT_PAR
NONE    = 0     # no board in slot
L1250   = 1
N1250   = 2
L1251   = 3
L1221   = 4
PCIA    = 5
PCIB    = 6
L264    = 8
L305    = 9
L1450C  = 10
L1450   = 11
L032    = 12
HI8     = 13
PCIC    = 14
LYNX2   = 15
TIGER2  = 16
TIGER3  = 17
LION    = 18
L791    = 19
LCPI    = 20
E440    = 30
E140    = 31
E2010   = 32
E270    = 33
CAN_USB = 34
AK9     = 35
LTR010  = 36
LTR021  = 37
E154    = 38
E2010B  = 39
LTR031  = 40
LTR030  = 41
E310    = 77
CA01    = 90


ErrorCode = {
        0: 'L_SUCCESS',            # функция выполнена успешно
        1: 'L_NOTSUPPORTED',       # функция не поддерживается этой платой
        2: 'L_ERROR',              # ошибка при выполнении функции
        3: 'L_ERROR_NOBOARD',      # нет платы в запрашиваемом слоте
        4: 'L_ERROR_INUSE',        # плата в запрашиваемом слоте уже используется
        5: 'L_ERROR_TIMEOUT'
    }

# Тип потока
L_STREAM_NULL   = 0
L_STREAM_ADC    = 1
L_STREAM_DAC    = 2
L_STREAM_TTLIN  = 3
L_STREAM_TTLOUT = 4
L_STREAM_FMETER = 5
L_STREAM_DDS    = 6

L_MEM_ALLOC     = 10        # смещение в массиве overlapped структур для overlapped аллокатора пямяти + stream_id

L_STREAM_ADC_ERROR = 0      # ERROR BITS FOR _EX interface + 0x20000000 for actual code
L_STREAM_DAC_ERROR = 1      # ERROR BITS FOR _EX interface + 0x20000000 for actual code

# define s_Type for FillDAQparameters
L_ADC_PARAM     = 1         # трактовать DAQ_PAR как ADC_PAR при передаче в FillDAQparameters
L_DAC_PARAM     = 2         # трактовать DAQ_PAR как DAC_PAR при передаче в FillDAQparameters
L_ASYNC_ADC_CFG = 3         # ASYNC_PAR содержит запрос на конфигурирование АЦП
L_ASYNC_TTL_CFG = 4         # ASYNC_PAR содержит запрос на конфигурирование цифровых линий
L_ASYNC_DAC_CFG = 5         # ASYNC_PAR содержит запрос на конфигурирование ЦАП
L_ASYNC_ADC_INP = 6         # ASYNC_PAR содержит запрос на ввод данных с АЦП
L_ASYNC_TTL_INP = 7         # ASYNC_PAR содержит запрос на ввод данных с цифровых линий
L_ASYNC_TTL_OUT = 8         # ASYNC_PAR содержит запрос на вывод данных на цифровые линии
L_ASYNC_DAC_OUT = 9         # ASYNC_PAR содержит запрос на вывод данных на ЦАП
L_ASYNC_FREQ_IN = 10
L_DDS_FM_PARAM  = 11

# Некоторые параметры для GetParameter/SetParameter
L_BOARD_TYPE    = 10000     # собственно поле sl.BoardType
L_POINT_SIZE    = 10001     # размер в байтах отсчета АЦП
L_SYNC_ADDR_LO  = 10002     # адрес переменной sync (счетчик АЦП)
L_SYNC_ADDR_HI  = 10003     # адрес переменной sync (счетчик АЦП)
L_DATA_ADDR_LO  = 10004     # адрес массива data ( АЦП)
L_DATA_ADDR_HI  = 10005     # адрес массива data ( АЦП)
L_SYNC1_ADDR_LO = 10006     # адрес переменной sync (счетчик ЦАП)
L_SYNC1_ADDR_HI = 10007     # адрес переменной sync (счетчик ЦАП)
L_DATA1_ADDR_LO = 10008     # адрес массива data ( ЦАП)
L_DATA1_ADDR_HI = 10009     # адрес массива data ( ЦАП)
L_USER_BASE     = 10100     # ранее сохраненные любые пользовательские 128 ULONG числа

# Определения EventId для событий SetLDeviceEvent
L_EVENT_ADC_BUF  = 1
L_EVENT_DAC_BUF  = 2
L_EVENT_ADC_OVF  = 3
L_EVENT_ADC_FIFO = 4
L_EVENT_DAC_USER = 5
L_EVENT_DAC_UNF  = 6
L_EVENT_PWR_OVR  = 7


class PORT_PAR(Structure):
    _pack_ = 1
    _fields_ = [
        ('port', c_uint),
        ('datatype', c_uint)
    ]


class SLOT_PAR(Structure):
    """ Структура, описывающая параметры виртуального слота """

    _pack_ = 1
    _fields_ = [
        ('Base', c_uint),           # базовый адрес первого региона портов
        ('BaseL', c_uint),          # протяженность первого региона портов в байтах
        ('Base1', c_uint),          # базовый адрес второго региона портов
        ('BaseL1', c_uint),         # протяженность второго региона портов в байтах
        ('Mem', c_uint),            # адрес первого региона памяти
        ('MemL', c_uint),           # протяженность первого региона памяти в байтах
        ('Mem1', c_uint),           # адрес второго региона памяти
        ('MemL1', c_uint),          # протяженность второго региона памяти в байтах
        ('Irq', c_uint),            # используемое драйвером аппаратное прерывание
        ('BoardType', c_uint),      # тип платы
        ('DSPType', c_uint),        # тип установленного на плате DSP
        ('Dma', c_uint),            # используемый для ввода данных канал ПДП: 0 - не использовать,5,6
        ('DmaDac', c_uint),         # используемый для вывода данных канал ПДП: 0 - не использовать,6
        ('DTA_REG', c_uint),
        ('IDMA_REG', c_uint),
        ('CMD_REG', c_uint),
        ('IRQ_RST', c_uint),
        ('DTA_ARRAY', c_uint),
        ('RDY_REG', c_uint),
        ('CFG_REG', c_uint)         # адреса регистров платы относительного базового адреса
    ]


class PLATA_DESCR(Structure):
    """ Структура, описывающая FLASH на PCI платах L-761/L-780/L-783 """

    _pack_ = 1
    _fields_ = [
        ('SerNum', c_char * 9),           # серийный номер платы
        ('BrdName', c_char * 5),          # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 5),          # тип DSP
        ('Quartz', c_uint),               # частота кварца
        ('IsDacPresent', c_ushort),       # наличие ЦАП
        ('Reserv1', c_ushort * 7),        # зарезервировано
        ('KoefADC', c_ushort * 8),        # калибровочные коэф. АЦП
        ('KoefDAC', c_ushort * 4),        # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 32)         # пользовательское место
    ]


class PLATA_DESCR_1450(Structure):
    """ Структура, описывающая FLASH на ISA плате L-1450 """

    _pack_ = 1
    _fields_ = [
        ('SerNum', c_char * 9),           # серийный номер платы
        ('BrdName', c_char * 7),          # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 5),          # тип DSP
        ('IsDacPresent', c_char),         # наличие ЦАП
        ('IsExtMemPresent', c_char),      # наличие внешней памяти данных
        ('Quartz', c_uint),               # частота кварца
        ('Reserv1', c_ushort * 6),        # зарезервировано
        ('KoefADC', c_ushort * 8),        # калибровочные коэф. АЦП
        ('KoefDAC', c_ushort * 4),        # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 32)         # пользовательское место
    ]


class PLATA_DESCR_L791(Structure):
    """ Структура, описывающая FLASH на PCI плате L-791 """

    _pack_ = 1
    _fields_ = [
        ('CRC16', c_ushort),              # контрольная сумма
        ('SerNum', c_char * 16),          # серийный номер платы
        ('BrdName', c_char * 16),         # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 5),          # тип DSP
        ('Quartz', c_uint),               # частота кварца
        ('IsDacPresent', c_ushort),       # наличие ЦАП
        ('KoefADC', c_float * 16),        # калибровочные коэф. АЦП
        ('KoefDAC', c_float * 4),         # калибровочные коэф. ЦАП
        ('Custom', c_ushort)              # пользовательское место
    ]


class PLATA_DESCR_E440(Structure):
    """ Структура, описывающая FLASH на USB модуле E14-440 """

    _pack_ = 1
    _fields_ = [
        ('SerNum', c_char * 9),           # серийный номер платы
        ('BrdName', c_char * 7),          # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 5),          # тип DSP
        ('IsDacPresent', c_char),         # наличие ЦАП
        ('Quartz', c_uint),               # частота кварца
        ('Reserv2', c_char * 13),         # зарезервировано
        ('KoefADC', c_ushort * 8),        # калибровочные коэф. АЦП
        ('KoefDAC', c_ushort * 4),        # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 32)         # пользовательское место
    ]


class PLATA_DESCR_E140(Structure):
    """ Структура, описывающая FLASH на USB модуле E14-140 """

    _pack_ = 1
    _fields_ = [
        ('SerNum', c_char * 9),           # серийный номер платы
        ('BrdName', c_char * 11),         # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 11),         # тип DSP
        ('IsDacPresent', c_char),         # наличие ЦАП
        ('Quartz', c_uint),               # частота кварца
        ('Reserv2', c_char * 3),          # зарезервировано
        ('KoefADC', c_float * 8),         # калибровочные коэф. АЦП
        ('KoefDAC', c_float * 4),         # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 20)         # пользовательское место
    ]


class PACKED_PLATA_DESCR_E140(Structure):
    _pack_ = 1
    _fields_ = [
        ('SerNum1', c_ubyte),             # серийный номер платы
        ('SerNum2', c_char),              # серийный номер платы
        ('SerNum3', c_uint),              # серийный номер платы
        ('Name', c_char * 10),            # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 10),         # тип DSP
        ('Quartz', c_uint),               # частота кварца
        ('CRC1', c_ubyte),
        ('IsDacPresent', c_ubyte),        # наличие ЦАП
        ('AdcOffs', c_float * 4),
        ('AdcScale', c_float * 4),
        ('DacOffs', c_float * 2),
        ('DacScale', c_float * 2),
        ('Reserv', c_ubyte * 46),         # зарезервировано
        ('CRC2', c_ubyte)
    ]


class PLATA_DESCR_E2010(Structure):
    """ Структура, описывающая FLASH на USB модуле E20-10 """

    _pack_ = 1
    _fields_ = [
        ('BrdName', c_char * 16),         # название платы
        ('SerNum', c_char * 16),          # серийный номер платы
        ('DspType', c_char * 16),         # тип DSP
        ('Quartz', c_uint),               # частота кварца
        ('Rev', c_char),                  # ревизия платы
        ('IsDacPresent', c_char),         # наличие ЦАП
        ('KoefADC', c_float * 24),        # калибровочные коэф. АЦП
        ('KoefDAC', c_float * 4),         # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 44),        # пользовательское место
        ('CRC', c_ushort)                 # контрольная сумма
    ]


class PLATA_DESCR_E154(Structure):
    """ Структура, описывающая FLASH на USB модуле E154 """

    _pack_ = 1
    _fields_ = [
        ('SerNum', c_char * 9),           # серийный номер платы
        ('BrdName', c_char * 11),         # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 11),         # тип DSP
        ('IsDacPresent', c_char),         # наличие ЦАП
        ('Quartz', c_uint),               # частота кварца
        ('Reserv2', c_char * 3),          # зарезервировано
        ('KoefADC', c_float * 8),         # калибровочные коэф. АЦП
        ('KoefDAC', c_float * 4),         # калибровочные коэф. ЦАП
        ('Custom', c_ushort * 20)         # пользовательское место
    ]


class PACKED_PLATA_DESCR_E154(Structure):
    _pack_ = 1
    _fields_ = [
        ('SerNum1', c_ubyte),             # серийный номер платы
        ('SerNum2', c_char),              # серийный номер платы
        ('SerNum3', c_uint),              # серийный номер платы
        ('Name', c_char * 10),            # название платы
        ('Rev', c_char),                  # ревизия платы
        ('DspType', c_char * 10),         # тип DSP
        ('Quartz', c_uint),               # частота кварца
        ('CRC1', c_ubyte),
        ('IsDacPresent', c_ubyte),        # наличие ЦАП
        ('AdcOffs', c_float * 4),
        ('AdcScale', c_float * 4),
        ('DacOffs', c_float * 2),
        ('DacScale', c_float * 2),
        ('Reserv', c_ubyte * 46),         # зарезервировано
        ('CRC2', c_ubyte)
    ]


class PLATA_DESCR_E310(Structure):
    """ Структура, описывающая FLASH на модуле E310 """

    _pack_ = 1
    _fields_ = [
        ('BrdName', c_char * 16),         # название платы
        ('SerNum', c_char * 16),          # серийный номер платы
        ('DspType', c_char * 25),         # тип DSP
        ('Rev', c_char),                  # ревизия платы
        ('Quartz', c_uint),               # частота кварца
        ('Reserved', c_char * 192),       # зарезервировано
        ('CRC', c_ushort)                 # контрольная сумма структуры
    ]


class E310_HW_PARAM(Structure):
    _pack_ = 1
    _fields_ = [
        ('DDS_CtrlReg', c_ushort),
        ('IncStepsReg', c_ushort),
        ('LoDeltaFreqReg', c_ushort),
        ('HiDeltaFreqReg', c_ushort),
        ('IncIntervalReg', c_ushort),
        ('LoStartFreqReg', c_ushort),
        ('HiStartFreqReg', c_ushort),
        ('LoStopFreqReg', c_ushort),
        ('HiStopFreqReg', c_ushort),
        ('AutoScanType', c_ubyte),
        ('MasterClock', c_double),
        ('Reserved0', c_ubyte * 15),
        ('CtrlReg', c_ubyte),
        ('OUT_10_OFFSET', c_ushort),
        ('FM_POROG', c_ushort),
        ('FM_Ena', c_ubyte),
        ('FM_Mode', c_ubyte),
        ('FM_InDiv', c_ubyte),
        ('FM_BCR_DivIdx', c_ubyte),
        ('FM_ClockRate', c_uint),
        ('FM_BCR', c_uint),
        ('Reserved1', c_ubyte * 21)
    ]


class E310_TTL_PARAM(Structure):
    _pack_ = 1
    _fields_ = [
        ('Mode', c_ubyte),
        ('Param', c_ushort),
        ('inTTL', c_ushort),
        ('outTTL', c_ushort),
        ('outTTL', c_ushort),
        ('Reserved', c_ubyte * 9)
    ]


class E310_ADC_PARAM(Structure):
    _pack_ = 1
    _fields_ = [
        ('StartSrc', c_ubyte),
        ('ChMask', c_ubyte),
        ('Reserved', c_ubyte * 5)
    ]


class WORD_IMAGE(Structure):
    """ Представление структуры FLASH в виде массива слов """

    _pack_ = 1
    _fields_ = [
        ('data', c_ushort * 64)
    ]


class BYTE_IMAGE(Structure):
    _pack_ = 1
    _fields_ = [
        ('data', c_ubyte * 128)
    ]


class WORD_IMAGE_256(Structure):
    _pack_ = 1
    _fields_ = [
        ('data', c_ushort * 128)
    ]


class BYTE_IMAGE_256(Structure):
    _pack_ = 1
    _fields_ = [
        ('data', c_ubyte * 256)
    ]


class PLATA_DESCR_U(Union):
    """ Обобщенная структура для удобства работы с флешами разных плат """

    _pack_ = 1
    _fields_ = [
        ('t1', PLATA_DESCR),
        ('t2', PLATA_DESCR_1450),
        ('t3', PLATA_DESCR_L791),
        ('t4', PLATA_DESCR_E440),
        ('t5', PLATA_DESCR_E140),
        ('pt5', PACKED_PLATA_DESCR_E140),
        ('wi', WORD_IMAGE),
        ('bi', BYTE_IMAGE)
    ]


class PLATA_DESCR_U2(Union):
    """ Обобщенная структура для удобства работы с флешами разных плат """

    _pack_ = 1
    _fields_ = [
        ('t1', PLATA_DESCR),
        ('t2', PLATA_DESCR_1450),
        ('t3', PLATA_DESCR_L791),
        ('t4', PLATA_DESCR_E440),
        ('t5', PLATA_DESCR_E140),
        ('pt5', PACKED_PLATA_DESCR_E140),
        ('t6', PLATA_DESCR_E2010),
        ('t7', PLATA_DESCR_E154),
        ('pt7', PACKED_PLATA_DESCR_E154),
        ('pt8', PLATA_DESCR_E310),
        ('wi', WORD_IMAGE),
        ('bi', BYTE_IMAGE),
        ('wi256', WORD_IMAGE_256),
        ('bi256', BYTE_IMAGE_256)
    ]


class IOCTL_BUFFER(Structure):
    """ Структура для доступа через ioctl """

    _pack_ = 1
    _fields_ = [
        ('inSize', c_int),                  # size in bytes
        ('outSize', c_int),                 # size in bytes
        ('inBuffer', c_ubyte * 4096),
        ('outBuffer', c_ubyte * 4096)
    ]


class DAQ_PAR(Structure):
    """ Базовая структура для описания параметров сбора данных """

    _pack_ = 1
    _fields_ = [
        ('s_Type', c_uint),                 # тип структуры
        ('FIFO', c_uint),                   # размер половины аппаратного буфера FIFO на плате
        ('IrqStep', c_uint),                # шаг генерации прерываний
        ('Pages', c_uint)                   # размер кольцевого буфера в шагах прерываний
    ]


class ADC_PAR_0(DAQ_PAR):
    """ Структура, служащая для передачи параметров сбора данных в плату """

    _pack_ = 1
    _fields_ = [
        ('AutoInit', c_uint),               # флаг, указывающий на тип сбора данных 0 - однократный 1 - циклический
        ('dRate', c_double),                # частота опроса каналов в кадре (кГц)
        ('dKadr', c_double),                # интервал между кадрами (мс)
        ('dScale', c_double),               # масштаб работы таймера для 1250 или делителя для 1221
        ('Rate', c_uint),                   # частота опроса каналов в кадре (в кодах для процессора, вычисляется библиотекой)
        ('Kadr', c_uint),                   # интервал между кадрами (в кодах для процессора, вычисляется библиотекой)
        ('Scale', c_uint),                  # масштаб работы таймера для 1250 или делителя для 1221 (в кодах для процессора, вычисляется библиотекой)
        ('FPDelay', c_uint),                # служебная величина задержки выдачи первого отсчета (вычисляется библиотекой)
        ('SynchroType', c_uint),            # тип синхронизации
        ('SynchroSensitivity', c_uint),     # вид синхронизации
        ('SynchroMode', c_uint),            # режим синхронизации
        ('AdChannel', c_uint),              # канал, по которому выполняется синхронизация
        ('AdPorog', c_uint),                # уровень синхронизации
        ('NCh', c_uint),                    # количество опрашиваемых каналов
        ('Chn', c_uint * 128),              # массив с номерами каналов и усилением на них. Описывает порядок опроса каналов
        ('IrqEna', c_uint),                 # разрешение генерации прерывания от платы (1/0)
        ('AdcEna', c_uint)                  # разрешение работы АЦП (1/0)
    ]


class ADC_PAR_1(DAQ_PAR):
    """ Структура, служащая для передачи параметров сбора данных в плату """

    _pack_ = 1
    _fields_ = [
        ('AutoInit', c_uint),               # флаг, указывающий на тип сбора данных 0 - однократный 1 - циклический
        ('dRate', c_double),                # частота опроса каналов в кадре (кГц)
        ('dKadr', c_double),                # интервал между кадрами (мс)
        ('Reserved1', c_ushort),            # зарезервировано
        ('DigRate', c_ushort),              # делитель частоты для цифрового потока
        ('DM_Ena', c_uint),                 # разрешение/запрещение маркировки данных
        ('Rate', c_uint),                   # частота опроса каналов в кадре (в кодах для цифрового автомата)
        ('Kadr', c_uint),                   # интервал между кадрами (в кодах для цифрового автомата)
        ('StartCnt', c_uint),               # задержка старта в кадрах
        ('StopCnt', c_uint),                # сколько кадров собирать после старта
        ('SynchroType', c_uint),            # тип синхронизации
        ('SynchroMode', c_uint),            # режим синхронизации и номер канала
        ('AdPorog', c_uint),                # порог синхронизации
        ('SynchroSrc', c_uint),             # источник внешней синхронизации
        ('AdcIMask', c_uint),               # задает режим ввода по каналам у модуля E2010
        ('NCh', c_uint),                    # количество опрашиваемых каналов
        ('Chn', c_uint * 128),              # массив с номерами каналов и усилением на них. Описывает порядок опроса каналов
        ('IrqEna', c_uint),                 # разрешение генерации прерывания от платы (1/0)
        ('AdcEna', c_uint)                  # разрешение работы АЦП (1/0)
    ]


class ADC_PAR(Union):
    """ Обобщенная структура для удобства работы со структурами задачи
        параметров сбора данных разных плат
    """

    _pack_ = 1
    _fields_ = [
        ('t1', ADC_PAR_0),
        ('t2', ADC_PAR_1)
    ]


class DAC_PAR_0(DAQ_PAR):
    """ Cтруктура для передачи параметров работы ЦАП в потоковом режиме """

    _pack_ = 1
    _fields_ = [
        ('AutoInit', c_uint),               # флаг, указывающий на тип сбора/выдачи данных 0 - однократный 1 - циклический; (пока не используется)
        ('dRate', c_double),                # частота вывода данных на ЦАП (кГц)
        ('Rate', c_uint),                   # частота вывода данных на ЦАП (в кодах для процессора)
        ('IrqEna', c_uint),                 # разрешение генерации прерывания от платы (1/0)
        ('DacEna', c_uint),                 # разрешение работы ЦAП (1/0)
        ('DacNumber', c_uint)               # номер канала ЦАП на который выводить данные
    ]


class DAC_PAR_1(DAQ_PAR):
    """ Cтруктура для передачи параметров работы ЦАП в потоковом режиме """

    _pack_ = 1
    _fields_ = [
        ('AutoInit', c_uint),               # флаг, указывающий на тип сбора данных 0 - однократный 1 - циклический; (пока не используется)
        ('dRate', c_double),                # частота вывода данных на ЦАП (кГц)
        ('Rate', c_uint),                   # частота вывода данных на ЦАП (в кодах для процессора)
        ('IrqEna', c_uint),                 # разрешение генерации прерывания от платы (1/0)
        ('DacEna', c_uint),                 # разрешение работы ЦAП (1/0)
        ('Reserved1', c_uint)
    ]


class DAC_PAR_2(DAQ_PAR):
    _pack_ = 1
    _fields_ = [
        ('MasterClk', c_double),
        ('MasterSrc', c_ushort),
        ('DDS_CtrlReg', c_ushort),
        ('CyclicScan', c_ubyte),
        ('ScanSteps', c_ushort),
        ('ScanFreqInc', c_double),
        ('ScanPeriodBase', c_ushort),
        ('ScanPeriodQnt', c_ushort),
        ('ScanPeriodMult', c_ushort),
        ('StartFreq', c_double),
        ('StopFreq', c_double),
        ('SyncOutType', c_ushort),
        ('SyncOutEna', c_ushort),
        ('TTLWaveEna', c_ubyte),
        ('IRQLineType', c_ubyte),
        ('ScanIncType', c_ushort),
        ('ScanCtrlType', c_ubyte),
        ('SignalForm', c_ushort),
        ('Out10_offset', c_double),
        ('Out10_offsrc', c_ubyte),
        ('OutGain', c_ubyte),
        ('FM_POROG', c_double),
        ('FM_Ena', c_ubyte),
        ('FM_Mode', c_ubyte),
        ('FM_InDiv', c_ubyte),
        ('FM_BCR_DivIdx', c_ubyte),
        ('FM_ClockRate', c_uint),
        ('FM_BCR', c_uint),
        ('Reserved1', c_ubyte * 21),
        ('dds_fm', E310_HW_PARAM)
    ]


class DAC_PAR(Union):
    """ Обобщенная структура для удобства работы со структурами параметров ЦАП """

    _pack_ = 1
    _fields_ = [
        ('t1', DAC_PAR_0),
        ('t2', DAC_PAR_1),
        ('t3', DAC_PAR_2)
    ]


class WDAC_PAR_0(Structure):
    _pack_ = 1
    _fields_ = [
        ('s_Type', c_uint),
        ('FIFO', c_uint),
        ('IrqStep', c_uint),
        ('Pages', c_uint),
        ('AutoInit', c_uint),
        ('dRate', c_double),
        ('Rate', c_uint),
        ('IrqEna', c_uint),
        ('DacEna', c_uint),
        ('DacNumber', c_uint)
    ]


class WDAC_PAR_1(Structure):
    _pack_ = 1
    _fields_ = [
        ('s_Type', c_uint),
        ('FIFO', c_uint),
        ('IrqStep', c_uint),
        ('Pages', c_uint),
        ('AutoInit', c_uint),
        ('dRate', c_double),
        ('Rate', c_uint),
        ('IrqEna', c_uint),
        ('DacEna', c_uint),
        ('Reserved1', c_uint)
    ]


class WADC_PAR_0(Structure):
    _pack_ = 1
    _fields_ = [
        ('s_Type', c_uint),
        ('FIFO', c_uint),
        ('IrqStep', c_uint),
        ('Pages', c_uint),
        ('AutoInit', c_uint),
        ('dRate', c_double),
        ('dKadr', c_double),
        ('dScale', c_double),
        ('Rate', c_uint),
        ('Kadr', c_uint),
        ('Scale', c_uint),
        ('FPDelay', c_uint),
        ('SynchroType', c_uint),
        ('SynchroSensitivity', c_uint),
        ('SynchroMode', c_uint),
        ('AdChannel', c_uint),
        ('AdPorog', c_uint),
        ('NCh', c_uint),
        ('Chn', c_uint * 128),
        ('IrqEna', c_uint),
        ('AdcEna', c_uint)
    ]


class WADC_PAR_1(Structure):
    _pack_ = 1
    _fields_ = [
        ('s_Type', c_uint),
        ('FIFO', c_uint),
        ('IrqStep', c_uint),
        ('Pages', c_uint),
        ('AutoInit', c_uint),
        ('dRate', c_double),
        ('dKadr', c_double),
        ('Reserved1', c_ushort),
        ('DigRate', c_ushort),
        ('DM_Ena', c_uint),
        ('Rate', c_uint),
        ('Kadr', c_uint),
        ('StartCnt', c_uint),
        ('StopCnt', c_uint),
        ('SynchroType', c_uint),
        ('SynchroMode', c_uint),
        ('AdPorog', c_uint),
        ('SynchroSrc', c_uint),
        ('AdcIMask', c_uint),
        ('NCh', c_uint),
        ('Chn', c_uint * 128),
        ('IrqEna', c_uint),
        ('AdcEna', c_uint)
    ]


class USHORT_IMAGE(Structure):
    _pack_ = 1
    _fields_ = [
        ('data', c_ushort * 512)
    ]


class WDAQ_PAR(Union):
    _pack_ = 1
    _fields_ = [
        ('t1', WDAC_PAR_0),
        ('t2', WDAC_PAR_1),
        ('t3', WADC_PAR_0),
        ('t4', WADC_PAR_1),
        ('wi', USHORT_IMAGE)
    ]


class ASYNC_PAR(DAQ_PAR):
    """ Cтруктура для передачи параметров асинхронного сбора/выдачи данных при вызове IoAsync """

    _pack_ = 1
    _fields_ = [
        ('dRate', c_double),                # частота опроса каналов в кадре (кГц)
        ('Rate', c_uint),                   # частота опроса каналов в кадре (в кодах для процессора)
        ('NCh', c_uint),                    # количество опрашиваемых каналов
        ('Chn', c_uint * 128),              # массив с номерами каналов и усилением на них. Описывает порядок опроса каналов
        ('Data', c_uint * 128),             # массив для данных
        ('Mode', c_uint)                    # задает различные режимы при конфигурации
    ]
