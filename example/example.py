#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from lcomp.lcomp import LCOMP
from lcomp.ldevioctl import (E140, E154, E440, E2010, E2010B, L791, L_ADC_PARAM,
                             L_ASYNC_ADC_INP, L_ASYNC_DAC_OUT, L_ASYNC_TTL_CFG,
                             L_ASYNC_TTL_INP, L_ASYNC_TTL_OUT, L_EVENT_ADC_BUF,
                             L_STREAM_ADC, L_USER_BASE, WASYNC_PAR, WDAQ_PAR)
from lcomp.device import e140, e154, e440, e2010, l791

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    with LCOMP(slot=0) as ldev:     # либо ldev.OpenLDevice() в начале и ldev.CloseLDevice() в конце
        print("LoadBios: {}".format(ldev.LoadBios("e2010m")))      # для E2010 биос "e2010", для E2010B биос "e2010m", для E440 биос "E440"
        print("PlataTest: {}".format(ldev.PlataTest()))

        slPar = ldev.GetSlotParam()
        print("GetSlotParam: {}".format(slPar))
        print("    Base:      {}".format(slPar.Base))
        print("    BaseL:     {}".format(slPar.BaseL))
        print("    Base1:     {}".format(slPar.Base1))
        print("    BaseL1:    {}".format(slPar.BaseL1))
        print("    Mem:       {}".format(slPar.Mem))
        print("    MemL:      {}".format(slPar.MemL))
        print("    Mem1:      {}".format(slPar.Mem1))
        print("    MemL1:     {}".format(slPar.MemL1))
        print("    Irq:       {}".format(slPar.Irq))
        print("    BoardType: {}".format(slPar.BoardType))
        print("    DSPType:   {}".format(slPar.DSPType))
        print("    Dma:       {}".format(slPar.Dma))
        print("    DmaDac:    {}".format(slPar.DmaDac))
        print("    DTA_REG:   {}".format(slPar.DTA_REG))
        print("    IDMA_REG:  {}".format(slPar.IDMA_REG))
        print("    CMD_REG:   {}".format(slPar.CMD_REG))
        print("    IRQ_RST:   {}".format(slPar.IRQ_RST))
        print("    DTA_ARRAY: {}".format(slPar.DTA_ARRAY))
        print("    RDY_REG:   {}".format(slPar.RDY_REG))
        print("    CFG_REG:   {}".format(slPar.CFG_REG))

        plDescr = ldev.ReadPlataDescr()
        print("ReadPlataDescr: {}".format(plDescr))

        if slPar.BoardType == E140:
            print("    SerNum:       {}".format(plDescr.t5.SerNum))
            print("    BrdName:      {}".format(plDescr.t5.BrdName))
            print("    Rev:          {}".format(plDescr.t5.Rev))
            print("    DspType:      {}".format(plDescr.t5.DspType))
            print("    IsDacPresent: {}".format(bool(plDescr.t5.IsDacPresent)))
            print("    Quartz:       {}".format(plDescr.t5.Quartz))
            # print("    KoefADC:      {}".format(list(plDescr.t5.KoefADC)))
            # print("    KoefDAC:      {}".format(list(plDescr.t5.KoefDAC)))
        elif slPar.BoardType == E440:
            print("    SerNum:       {}".format(plDescr.t4.SerNum))
            print("    BrdName:      {}".format(plDescr.t4.BrdName))
            print("    Rev:          {}".format(plDescr.t4.Rev))
            print("    DspType:      {}".format(plDescr.t4.DspType))
            print("    IsDacPresent: {}".format(bool(plDescr.t4.IsDacPresent)))
            print("    Quartz:       {}".format(plDescr.t4.Quartz))
            # print("    KoefADC:      {}".format(list(plDescr.t4.KoefADC)))
            # print("    KoefDAC:      {}".format(list(plDescr.t4.KoefDAC)))
        elif slPar.BoardType == E154:
            print("    SerNum:       {}".format(plDescr.t7.SerNum))
            print("    BrdName:      {}".format(plDescr.t7.BrdName))
            print("    Rev:          {}".format(plDescr.t7.Rev))
            print("    DspType:      {}".format(plDescr.t7.DspType))
            print("    IsDacPresent: {}".format(bool(plDescr.t7.IsDacPresent)))
            print("    Quartz:       {}".format(plDescr.t7.Quartz))
            # print("    KoefADC:      {}".format(list(plDescr.t7.KoefADC)))
            # print("    KoefDAC:      {}".format(list(plDescr.t7.KoefDAC)))
        elif slPar.BoardType in (E2010, E2010B):
            print("    SerNum:       {}".format(plDescr.t6.SerNum))
            print("    BrdName:      {}".format(plDescr.t6.BrdName))
            print("    Rev:          {}".format(plDescr.t6.Rev))
            print("    DspType:      {}".format(plDescr.t6.DspType))
            print("    IsDacPresent: {}".format(bool(plDescr.t6.IsDacPresent)))
            print("    Quartz:       {}".format(plDescr.t6.Quartz))
            # print("    KoefADC:      {}".format(list(plDescr.t6.KoefADC)))
            # print("    KoefDAC:      {}".format(list(plDescr.t6.KoefDAC)))
        elif slPar.BoardType == L791:
            print("    SerNum:       {}".format(plDescr.t3.SerNum))
            print("    BrdName:      {}".format(plDescr.t3.BrdName))
            print("    Rev:          {}".format(plDescr.t3.Rev))
            print("    DspType:      {}".format(plDescr.t3.DspType))
            print("    IsDacPresent: {}".format(bool(plDescr.t3.IsDacPresent)))
            print("    Quartz:       {}".format(plDescr.t3.Quartz))
            # print("    KoefADC:      {}".format(list(plDescr.t3.KoefADC)))
            # print("    KoefDAC:      {}".format(list(plDescr.t3.KoefDAC)))

        # Потоковый вывод с АЦП

        buffer_size = ldev.RequestBufferStream(size=131072, stream_id=L_STREAM_ADC)    # Желательно, чтобы размер буфера был
        print("RequestBufferStream: {}".format(buffer_size))                           # кратен числу используемых каналов NCh

        if slPar.BoardType in (E140, E440, E154):
            adcPar = WDAQ_PAR()

            adcPar.t3.s_Type = L_ADC_PARAM
            adcPar.t3.FIFO = 4096
            adcPar.t3.IrqStep = 4096
            adcPar.t3.Pages = 32
            adcPar.t3.AutoInit = 0                              # Для E440:                 Для E154:
            adcPar.t3.dRate = 100.0                             # 400.0                     100.0
            adcPar.t3.dKadr = 0.01                              # 0.0025                    0.01
            adcPar.t3.SynchroType = e140.NO_SYNC                # e440.NO_SYNC              e154.NO_SYNC
            adcPar.t3.SynchroSensitivity = e140.A_SYNC_LEVEL    # e440.A_SYNC_LEVEL         e154.A_SYNC_LEVEL
            adcPar.t3.SynchroMode = e140.A_SYNC_UP_EDGE         # e440.A_SYNC_UP_EDGE       e154.A_SYNC_UP_EDGE
            adcPar.t3.AdChannel = 0
            adcPar.t3.AdPorog = 0
            adcPar.t3.NCh = 1                                   # 1 - 16                    1 - 8
            adcPar.t3.Chn[0] = e140.CH_0 | e140.V10000 | e140.CH_DIFF     # для дифференциального режима
            # adcPar.t3.Chn[0] = e140.CH_0 | e140.V10000 | e140.CH_GRND   # для режима с общей землей

            # adcPar.t3.Chn[1] = e140.CH_1 | e140.V2500         # e440.CH_1 | e440.V2500    e154.CH_1 | e154.V1600
            # adcPar.t3.Chn[2] = e140.CH_2 | e140.V0625         # e440.CH_2 | e440.V0625    e154.CH_2 | e154.V0500
            # adcPar.t3.Chn[3] = e140.CH_3 | e140.V0156         # e440.CH_3 | e440.V0156    e154.CH_3 | e154.V0160
            adcPar.t3.IrqEna = 1
            adcPar.t3.AdcEna = 1

            print("FillDAQparameters: {}".format(ldev.FillDAQparameters(adcPar.t3)))
            print("    s_Type:             {}".format(adcPar.t3.s_Type))
            print("    FIFO:               {}".format(adcPar.t3.FIFO))
            print("    IrqStep:            {}".format(adcPar.t3.IrqStep))
            print("    Pages:              {}".format(adcPar.t3.Pages))
            print("    AutoInit:           {}".format(adcPar.t3.AutoInit))
            print("    dRate:              {}".format(adcPar.t3.dRate))
            print("    dKadr:              {}".format(adcPar.t3.dKadr))
            print("    dScale:             {}".format(adcPar.t3.dScale))
            print("    Rate:               {}".format(adcPar.t3.Rate))
            print("    Kadr:               {}".format(adcPar.t3.Kadr))
            print("    Scale:              {}".format(adcPar.t3.Scale))
            print("    FPDelay:            {}".format(adcPar.t3.FPDelay))
            print("    SynchroType:        {}".format(adcPar.t3.SynchroType))
            print("    SynchroSensitivity: {}".format(adcPar.t3.SynchroSensitivity))
            print("    SynchroMode:        {}".format(adcPar.t3.SynchroMode))
            print("    AdChannel:          {}".format(adcPar.t3.AdChannel))
            print("    AdPorog:            {}".format(adcPar.t3.AdPorog))
            print("    NCh:                {}".format(adcPar.t3.NCh))
            # print("    Chn:                {}".format(list(adcPar.t3.Chn)))
            print("    IrqEna:             {}".format(adcPar.t3.IrqEna))
            print("    AdcEna:             {}".format(adcPar.t3.AdcEna))

            data_ptr, syncd = ldev.SetParametersStream(adcPar.t3, buffer_size)
            print("SetParametersStream: {}, {}".format(data_ptr, syncd))
            print("    Pages:   {}".format(adcPar.t3.Pages))
            print("    IrqStep: {}".format(adcPar.t3.IrqStep))
            print("    FIFO:    {}".format(adcPar.t3.FIFO))
            print("    Rate:    {}".format(adcPar.t3.dRate))

        elif slPar.BoardType in (E2010, E2010B):
            adcPar = WDAQ_PAR()

            adcPar.t4.s_Type = L_ADC_PARAM
            adcPar.t4.FIFO = 4096
            adcPar.t4.IrqStep = 4096
            adcPar.t4.Pages = 32
            adcPar.t4.AutoInit = 0
            adcPar.t4.dRate = 1000.0
            adcPar.t4.dKadr = 0.001
            adcPar.t4.SynchroType = e2010.INT_START_TRANS
            adcPar.t4.SynchroSrc = e2010.INT_CLK_TRANS
            adcPar.t4.AdcIMask = e2010.SIG_0 | e2010.V30_0  # | e2010.SIG_1 | e2010.V10_1 # | e2010.SIG_2 | e2010.V03_2 # | e2010.GND_3
            adcPar.t4.NCh = 1   # 1 - 4
            adcPar.t4.Chn[0] = e2010.CH_0
            # adcPar.t4.Chn[1] = e2010.CH_1
            # adcPar.t4.Chn[2] = e2010.CH_2
            # adcPar.t4.Chn[3] = e2010.CH_3
            adcPar.t4.IrqEna = 1
            adcPar.t4.AdcEna = 1

            print("FillDAQparameters: {}".format(ldev.FillDAQparameters(adcPar.t4)))
            print("    s_Type:      {}".format(adcPar.t4.s_Type))
            print("    FIFO:        {}".format(adcPar.t4.FIFO))
            print("    IrqStep:     {}".format(adcPar.t4.IrqStep))
            print("    Pages:       {}".format(adcPar.t4.Pages))
            print("    AutoInit:    {}".format(adcPar.t4.AutoInit))
            print("    dRate:       {}".format(adcPar.t4.dRate))
            print("    dKadr:       {}".format(adcPar.t4.dKadr))
            print("    Reserved1:   {}".format(adcPar.t4.Reserved1))
            print("    DigRate:     {}".format(adcPar.t4.DigRate))
            print("    DM_Ena:      {}".format(adcPar.t4.DM_Ena))
            print("    Rate:        {}".format(adcPar.t4.Rate))
            print("    Kadr:        {}".format(adcPar.t4.Kadr))
            print("    StartCnt:    {}".format(adcPar.t4.StartCnt))
            print("    StopCnt:     {}".format(adcPar.t4.StopCnt))
            print("    SynchroType: {}".format(adcPar.t4.SynchroType))
            print("    SynchroMode: {}".format(adcPar.t4.SynchroMode))
            print("    AdPorog:     {}".format(adcPar.t4.AdPorog))
            print("    SynchroSrc:  {}".format(adcPar.t4.SynchroSrc))
            print("    AdcIMask:    {}".format(adcPar.t4.AdcIMask))
            print("    NCh:         {}".format(adcPar.t4.NCh))
            # print("    Chn:         {}".format(list(adcPar.t4.Chn)))
            print("    IrqEna:      {}".format(adcPar.t4.IrqEna))
            print("    AdcEna:      {}".format(adcPar.t4.AdcEna))

            data_ptr, syncd = ldev.SetParametersStream(adcPar.t4, buffer_size)
            print("SetParametersStream: {}, {}".format(data_ptr, syncd))
            print("    Pages:   {}".format(adcPar.t4.Pages))
            print("    IrqStep: {}".format(adcPar.t4.IrqStep))
            print("    FIFO:    {}".format(adcPar.t4.FIFO))
            print("    Rate:    {}".format(adcPar.t4.dRate))

        elif slPar.BoardType == L791:
            adcPar = WDAQ_PAR()

            adcPar.t4.s_Type = L_ADC_PARAM
            adcPar.t4.FIFO = 128
            adcPar.t4.IrqStep = 1024
            adcPar.t4.Pages = 128
            adcPar.t4.AutoInit = 0
            adcPar.t4.dRate = 200.0
            adcPar.t4.dKadr = 0.005
            adcPar.t4.SynchroType = 0
            adcPar.t4.SynchroSrc = 0
            adcPar.t4.NCh = 1   # 1 - 16
            adcPar.t4.Chn[0] = l791.CH_0 | l791.V10000
            # adcPar.t4.Chn[1] = l791.CH_1 | l791.V5000
            # adcPar.t4.Chn[2] = l791.CH_2 | l791.V2500
            # adcPar.t4.Chn[3] = l791.CH_3 | l791.V1250
            adcPar.t4.IrqEna = 1
            adcPar.t4.AdcEna = 1

            print("FillDAQparameters: {}".format(ldev.FillDAQparameters(adcPar.t4)))
            print("    s_Type:      {}".format(adcPar.t4.s_Type))
            print("    FIFO:        {}".format(adcPar.t4.FIFO))
            print("    IrqStep:     {}".format(adcPar.t4.IrqStep))
            print("    Pages:       {}".format(adcPar.t4.Pages))
            print("    AutoInit:    {}".format(adcPar.t4.AutoInit))
            print("    dRate:       {}".format(adcPar.t4.dRate))
            print("    dKadr:       {}".format(adcPar.t4.dKadr))
            print("    Reserved1:   {}".format(adcPar.t4.Reserved1))
            print("    DigRate:     {}".format(adcPar.t4.DigRate))
            print("    DM_Ena:      {}".format(adcPar.t4.DM_Ena))
            print("    Rate:        {}".format(adcPar.t4.Rate))
            print("    Kadr:        {}".format(adcPar.t4.Kadr))
            print("    StartCnt:    {}".format(adcPar.t4.StartCnt))
            print("    StopCnt:     {}".format(adcPar.t4.StopCnt))
            print("    SynchroType: {}".format(adcPar.t4.SynchroType))
            print("    SynchroMode: {}".format(adcPar.t4.SynchroMode))
            print("    AdPorog:     {}".format(adcPar.t4.AdPorog))
            print("    SynchroSrc:  {}".format(adcPar.t4.SynchroSrc))
            print("    AdcIMask:    {}".format(adcPar.t4.AdcIMask))
            print("    NCh:         {}".format(adcPar.t4.NCh))
            # print("    Chn:         {}".format(list(adcPar.t4.Chn)))
            print("    IrqEna:      {}".format(adcPar.t4.IrqEna))
            print("    AdcEna:      {}".format(adcPar.t4.AdcEna))

            data_ptr, syncd = ldev.SetParametersStream(adcPar.t4, buffer_size)
            print("SetParametersStream: {}, {}".format(data_ptr, syncd))
            print("    Pages:   {}".format(adcPar.t4.Pages))
            print("    IrqStep: {}".format(adcPar.t4.IrqStep))
            print("    FIFO:    {}".format(adcPar.t4.FIFO))
            print("    Rate:    {}".format(adcPar.t4.dRate))

        print("EnableCorrection: {}".format(ldev.EnableCorrection(True)))

        print("InitStartLDevice: {}".format(ldev.InitStartLDevice()))
        print("StartLDevice: {}".format(ldev.StartLDevice()))

        print("Read data from buffer ...")

        while syncd() < buffer_size:            # ждем, пока заполнится буфер
            pass

        print("Data ready ...")

        if slPar.BoardType == E140:
            x = e140.GetDataADC(adcPar.t3, plDescr, data_ptr, buffer_size)
        elif slPar.BoardType == E440:
            x = e440.GetDataADC(adcPar.t3, plDescr, data_ptr, buffer_size)
        elif slPar.BoardType == E154:
            x = e154.GetDataADC(adcPar.t3, plDescr, data_ptr, buffer_size)
        elif slPar.BoardType in (E2010, E2010B):
            x = e2010.GetDataADC(adcPar.t4, plDescr, data_ptr, buffer_size)
        elif slPar.BoardType == L791:
            x = l791.GetDataADC(adcPar.t4, plDescr, data_ptr, buffer_size)

        x[0].tofile("channel-1.log", sep="\n")  # индекс соответствует номеру канала из Chn
        # x[1].tofile("channel-2.log", sep="\n")
        # x[2].tofile("channel-3.log", sep="\n")

        print("StopLDevice: {}".format(ldev.StopLDevice()))

        # Асинхронные операции ввода/вывода

        asp = WASYNC_PAR()

        asp.s_Type = L_ASYNC_DAC_OUT
        asp.Mode = 0
        asp.Data[0] = 512
        if ldev.IoAsync(asp):
            print("IoAsync (L_ASYNC_DAC_OUT): {}".format(asp.Data[0]))

        asp.s_Type = L_ASYNC_ADC_INP
        asp.Chn[0] = 0x00
        if ldev.IoAsync(asp):
            print("IoAsync (L_ASYNC_ADC_INP): {}".format(asp.Data[0]))

        asp.s_Type = L_ASYNC_TTL_CFG
        asp.Mode = 1
        if ldev.IoAsync(asp):
            print("IoAsync (L_ASYNC_TTL_CFG): {}".format(asp.Data[0]))

        asp.s_Type = L_ASYNC_TTL_INP
        asp.Chn[0] = 0x00
        if ldev.IoAsync(asp):
            print("IoAsync (L_ASYNC_TTL_INP): {}".format(asp.Data[0]))

        asp.s_Type = L_ASYNC_TTL_OUT
        asp.Data[0] = 0xA525
        if ldev.IoAsync(asp):
            print("IoAsync (L_ASYNC_TTL_OUT): {}".format(asp.Data[0]))

        # Проверка работоспособности других функций

        print("SetParameter (L_USER_BASE): {}".format(ldev.SetParameter(name=L_USER_BASE, value=123)))
        print("GetParameter (L_USER_BASE): {}".format(ldev.GetParameter(name=L_USER_BASE)))
        print("ReadFlashWord: {}".format(ldev.ReadFlashWord(address=L_USER_BASE)))
        print("EnableFlashWrite: {}".format(ldev.EnableFlashWrite(False)))
        print("SendCommand: {}".format(ldev.SendCommand(cmd=0)))
        print("SetLDeviceEvent: {}".format(ldev.SetLDeviceEvent(event=0, event_id=L_EVENT_ADC_BUF)))

        print("GetWord_DM: {}".format(ldev.GetWord_DM(address=0x0400)))
        print("GetWord_PM: {}".format(ldev.GetWord_PM(address=0)))
        print("GetArray_DM: {}".format(ldev.GetArray_DM(address=0x1080, count=2)))
        print("GetArray_PM: {}".format(ldev.GetArray_PM(address=0, count=2)))

        print("inbyte: {}".format(ldev.inbyte(offset=0)))
        print("inword: {}".format(ldev.inword(offset=0)))
        print("indword: {}".format(ldev.indword(offset=0)))
        print("inmbyte: {}".format(ldev.inmbyte(offset=0)))
        print("inmword: {}".format(ldev.inmword(offset=0)))
        print("inmdword: {}".format(ldev.inmdword(offset=0)))

        print("Get_LDEV2_Interface: {}".format(ldev.Get_LDEV2_Interface()))
        print("InitStartLDeviceEx: {}".format(ldev.InitStartLDeviceEx(stream_id=L_STREAM_ADC)))
        print("StartLDeviceEx: {}".format(ldev.StartLDeviceEx(stream_id=L_STREAM_ADC)))
        print("StopLDeviceEx: {}".format(ldev.StopLDeviceEx(stream_id=L_STREAM_ADC)))
        print("Release_LDEV2_Interface: {}".format(ldev.Release_LDEV2_Interface()))
