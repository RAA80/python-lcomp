#! /usr/bin/env python3

"""Пример использования библиотеки."""

import logging

from lcomp.device import e140, e154, e440, e2010, l791
from lcomp.ioctl import (L_ASYNC, L_DEVICE, L_EVENT, L_PARAM, L_STREAM, L_USER_BASE,
                         WASYNC_PAR, WDAQ_PAR)
from lcomp.lcomp import LCOMP

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    with LCOMP(slot=0) as ldev:     # либо ldev.OpenLDevice() в начале и ldev.CloseLDevice() в конце
        print(f"LoadBios: {ldev.LoadBios('e2010m')}")       # для E2010 биос "e2010", для E2010B биос "e2010m", для E440 биос "E440"
        print(f"PlataTest: {ldev.PlataTest()}")

        slpar = ldev.GetSlotParam()
        print(f"GetSlotParam: {slpar}")
        print(f"    Base:      {slpar.Base}")
        print(f"    BaseL:     {slpar.BaseL}")
        print(f"    Base1:     {slpar.Base1}")
        print(f"    BaseL1:    {slpar.BaseL1}")
        print(f"    Mem:       {slpar.Mem}")
        print(f"    MemL:      {slpar.MemL}")
        print(f"    Mem1:      {slpar.Mem1}")
        print(f"    MemL1:     {slpar.MemL1}")
        print(f"    Irq:       {slpar.Irq}")
        print(f"    BoardType: {slpar.BoardType}")
        print(f"    DSPType:   {slpar.DSPType}")
        print(f"    Dma:       {slpar.Dma}")
        print(f"    DmaDac:    {slpar.DmaDac}")
        print(f"    DTA_REG:   {slpar.DTA_REG}")
        print(f"    IDMA_REG:  {slpar.IDMA_REG}")
        print(f"    CMD_REG:   {slpar.CMD_REG}")
        print(f"    IRQ_RST:   {slpar.IRQ_RST}")
        print(f"    DTA_ARRAY: {slpar.DTA_ARRAY}")
        print(f"    RDY_REG:   {slpar.RDY_REG}")
        print(f"    CFG_REG:   {slpar.CFG_REG}")

        descr = ldev.ReadPlataDescr()
        print(f"ReadPlataDescr: {descr}")

        if slpar.BoardType == L_DEVICE.E140:
            print(f"    SerNum:       {descr.t5.SerNum}")
            print(f"    BrdName:      {descr.t5.BrdName}")
            print(f"    Rev:          {descr.t5.Rev}")
            print(f"    DspType:      {descr.t5.DspType}")
            print(f"    IsDacPresent: {bool(descr.t5.IsDacPresent)}")
            print(f"    Quartz:       {descr.t5.Quartz}")
            # print(f"    KoefADC:      {list(descr.t5.KoefADC)}")
            # print(f"    KoefDAC:      {list(descr.t5.KoefDAC)}")
        elif slpar.BoardType == L_DEVICE.E440:
            print(f"    SerNum:       {descr.t4.SerNum}")
            print(f"    BrdName:      {descr.t4.BrdName}")
            print(f"    Rev:          {descr.t4.Rev}")
            print(f"    DspType:      {descr.t4.DspType}")
            print(f"    IsDacPresent: {bool(descr.t4.IsDacPresent)}")
            print(f"    Quartz:       {descr.t4.Quartz}")
            # print(f"    KoefADC:      {list(descr.t4.KoefADC)}")
            # print(f"    KoefDAC:      {list(descr.t4.KoefDAC)}")
        elif slpar.BoardType == L_DEVICE.E154:
            print(f"    SerNum:       {descr.t7.SerNum}")
            print(f"    BrdName:      {descr.t7.BrdName}")
            print(f"    Rev:          {descr.t7.Rev}")
            print(f"    DspType:      {descr.t7.DspType}")
            print(f"    IsDacPresent: {bool(descr.t7.IsDacPresent)}")
            print(f"    Quartz:       {descr.t7.Quartz}")
            # print(f"    KoefADC:      {list(descr.t7.KoefADC)}")
            # print(f"    KoefDAC:      {list(descr.t7.KoefDAC)}")
        elif slpar.BoardType in {L_DEVICE.E2010, L_DEVICE.E2010B}:
            print(f"    SerNum:       {descr.t6.SerNum}")
            print(f"    BrdName:      {descr.t6.BrdName}")
            print(f"    Rev:          {descr.t6.Rev}")
            print(f"    DspType:      {descr.t6.DspType}")
            print(f"    IsDacPresent: {bool(descr.t6.IsDacPresent)}")
            print(f"    Quartz:       {descr.t6.Quartz}")
            # print(f"    KoefADC:      {list(descr.t6.KoefADC)}")
            # print(f"    KoefDAC:      {list(descr.t6.KoefDAC)}")
        elif slpar.BoardType == L_DEVICE.L791:
            print(f"    SerNum:       {descr.t3.SerNum}")
            print(f"    BrdName:      {descr.t3.BrdName}")
            print(f"    Rev:          {descr.t3.Rev}")
            print(f"    DspType:      {descr.t3.DspType}")
            print(f"    IsDacPresent: {bool(descr.t3.IsDacPresent)}")
            print(f"    Quartz:       {descr.t3.Quartz}")
            # print(f"    KoefADC:      {list(descr.t3.KoefADC)}")
            # print(f"    KoefDAC:      {list(descr.t3.KoefDAC)}")

        # Потоковый вывод с АЦП

        buffer_size = ldev.RequestBufferStream(size=131072, stream_id=L_STREAM.ADC)     # Желательно, чтобы размер буфера был
        print(f"RequestBufferStream: {buffer_size}")                                    # кратен числу используемых каналов NCh

        if slpar.BoardType in {L_DEVICE.E140, L_DEVICE.E440, L_DEVICE.E154}:
            adcpar = WDAQ_PAR()

            adcpar.t3.s_Type = L_PARAM.ADC
            adcpar.t3.FIFO = 4096
            adcpar.t3.IrqStep = 4096
            adcpar.t3.Pages = 32
            adcpar.t3.AutoInit = 0                              # Для E440:                 Для E154:
            adcpar.t3.dRate = 100.0                             # 400.0                     100.0
            adcpar.t3.dKadr = 0.01                              # 0.0025                    0.01
            adcpar.t3.SynchroType = e140.NO_SYNC                # e440.NO_SYNC              e154.NO_SYNC
            adcpar.t3.SynchroSensitivity = e140.A_SYNC_LEVEL    # e440.A_SYNC_LEVEL         e154.A_SYNC_LEVEL
            adcpar.t3.SynchroMode = e140.A_SYNC_UP_EDGE         # e440.A_SYNC_UP_EDGE       e154.A_SYNC_UP_EDGE
            adcpar.t3.AdChannel = 0
            adcpar.t3.AdPorog = 0
            adcpar.t3.NCh = 1                                   # 1 - 16                    1 - 8
            adcpar.t3.Chn[0] = e140.CH_0 | e140.V10000 | e140.CH_DIFF     # для дифференциального режима
            # adcpar.t3.Chn[0] = e140.CH_0 | e140.V10000 | e140.CH_GRND   # для режима с общей землей

            # adcpar.t3.Chn[1] = e140.CH_1 | e140.V2500         # e440.CH_1 | e440.V2500    e154.CH_1 | e154.V1600
            # adcpar.t3.Chn[2] = e140.CH_2 | e140.V0625         # e440.CH_2 | e440.V0625    e154.CH_2 | e154.V0500
            # adcpar.t3.Chn[3] = e140.CH_3 | e140.V0156         # e440.CH_3 | e440.V0156    e154.CH_3 | e154.V0160
            adcpar.t3.IrqEna = 1
            adcpar.t3.AdcEna = 1

            print(f"FillDAQparameters: {ldev.FillDAQparameters(adcpar.t3)}")
            print(f"    s_Type:             {adcpar.t3.s_Type}")
            print(f"    FIFO:               {adcpar.t3.FIFO}")
            print(f"    IrqStep:            {adcpar.t3.IrqStep}")
            print(f"    Pages:              {adcpar.t3.Pages}")
            print(f"    AutoInit:           {adcpar.t3.AutoInit}")
            print(f"    dRate:              {adcpar.t3.dRate}")
            print(f"    dKadr:              {adcpar.t3.dKadr}")
            print(f"    dScale:             {adcpar.t3.dScale}")
            print(f"    Rate:               {adcpar.t3.Rate}")
            print(f"    Kadr:               {adcpar.t3.Kadr}")
            print(f"    Scale:              {adcpar.t3.Scale}")
            print(f"    FPDelay:            {adcpar.t3.FPDelay}")
            print(f"    SynchroType:        {adcpar.t3.SynchroType}")
            print(f"    SynchroSensitivity: {adcpar.t3.SynchroSensitivity}")
            print(f"    SynchroMode:        {adcpar.t3.SynchroMode}")
            print(f"    AdChannel:          {adcpar.t3.AdChannel}")
            print(f"    AdPorog:            {adcpar.t3.AdPorog}")
            print(f"    NCh:                {adcpar.t3.NCh}")
            # print(f"    Chn:                {list(adcpar.t3.Chn)}")
            print(f"    IrqEna:             {adcpar.t3.IrqEna}")
            print(f"    AdcEna:             {adcpar.t3.AdcEna}")

            data_ptr, syncd = ldev.SetParametersStream(adcpar.t3, buffer_size)
            print(f"SetParametersStream: {data_ptr}, {syncd}")
            print(f"    Pages:   {adcpar.t3.Pages}")
            print(f"    IrqStep: {adcpar.t3.IrqStep}")
            print(f"    FIFO:    {adcpar.t3.FIFO}")
            print(f"    Rate:    {adcpar.t3.dRate}")

        elif slpar.BoardType in {L_DEVICE.E2010, L_DEVICE.E2010B}:
            adcpar = WDAQ_PAR()

            adcpar.t4.s_Type = L_PARAM.ADC
            adcpar.t4.FIFO = 4096
            adcpar.t4.IrqStep = 4096
            adcpar.t4.Pages = 32
            adcpar.t4.AutoInit = 0
            adcpar.t4.dRate = 1000.0
            adcpar.t4.dKadr = 0.001
            adcpar.t4.SynchroType = e2010.INT_START_TRANS
            adcpar.t4.SynchroSrc = e2010.INT_CLK_TRANS
            adcpar.t4.AdcIMask = e2010.SIG_0 | e2010.V30_0  # | e2010.SIG_1 | e2010.V10_1 # | e2010.SIG_2 | e2010.V03_2 # | e2010.GND_3
            adcpar.t4.NCh = 1   # 1 - 4
            adcpar.t4.Chn[0] = e2010.CH_0
            # adcpar.t4.Chn[1] = e2010.CH_1
            # adcpar.t4.Chn[2] = e2010.CH_2
            # adcpar.t4.Chn[3] = e2010.CH_3
            adcpar.t4.IrqEna = 1
            adcpar.t4.AdcEna = 1

            print(f"FillDAQparameters: {ldev.FillDAQparameters(adcpar.t4)}")
            print(f"    s_Type:      {adcpar.t4.s_Type}")
            print(f"    FIFO:        {adcpar.t4.FIFO}")
            print(f"    IrqStep:     {adcpar.t4.IrqStep}")
            print(f"    Pages:       {adcpar.t4.Pages}")
            print(f"    AutoInit:    {adcpar.t4.AutoInit}")
            print(f"    dRate:       {adcpar.t4.dRate}")
            print(f"    dKadr:       {adcpar.t4.dKadr}")
            print(f"    Reserved1:   {adcpar.t4.Reserved1}")
            print(f"    DigRate:     {adcpar.t4.DigRate}")
            print(f"    DM_Ena:      {adcpar.t4.DM_Ena}")
            print(f"    Rate:        {adcpar.t4.Rate}")
            print(f"    Kadr:        {adcpar.t4.Kadr}")
            print(f"    StartCnt:    {adcpar.t4.StartCnt}")
            print(f"    StopCnt:     {adcpar.t4.StopCnt}")
            print(f"    SynchroType: {adcpar.t4.SynchroType}")
            print(f"    SynchroMode: {adcpar.t4.SynchroMode}")
            print(f"    AdPorog:     {adcpar.t4.AdPorog}")
            print(f"    SynchroSrc:  {adcpar.t4.SynchroSrc}")
            print(f"    AdcIMask:    {adcpar.t4.AdcIMask}")
            print(f"    NCh:         {adcpar.t4.NCh}")
            # print(f"    Chn:         {list(adcpar.t4.Chn)}")
            print(f"    IrqEna:      {adcpar.t4.IrqEna}")
            print(f"    AdcEna:      {adcpar.t4.AdcEna}")

            data_ptr, syncd = ldev.SetParametersStream(adcpar.t4, buffer_size)
            print(f"SetParametersStream: {data_ptr}, {syncd}")
            print(f"    Pages:   {adcpar.t4.Pages}")
            print(f"    IrqStep: {adcpar.t4.IrqStep}")
            print(f"    FIFO:    {adcpar.t4.FIFO}")
            print(f"    Rate:    {adcpar.t4.dRate}")

        elif slpar.BoardType == L_DEVICE.L791:
            adcpar = WDAQ_PAR()

            adcpar.t4.s_Type = L_PARAM.ADC
            adcpar.t4.FIFO = 128
            adcpar.t4.IrqStep = 1024
            adcpar.t4.Pages = 128
            adcpar.t4.AutoInit = 0
            adcpar.t4.dRate = 200.0
            adcpar.t4.dKadr = 0.005
            adcpar.t4.SynchroType = 0
            adcpar.t4.SynchroSrc = 0
            adcpar.t4.NCh = 1   # 1 - 16
            adcpar.t4.Chn[0] = l791.CH_0 | l791.V10000
            # adcpar.t4.Chn[1] = l791.CH_1 | l791.V5000
            # adcpar.t4.Chn[2] = l791.CH_2 | l791.V2500
            # adcpar.t4.Chn[3] = l791.CH_3 | l791.V1250
            adcpar.t4.IrqEna = 1
            adcpar.t4.AdcEna = 1

            print(f"FillDAQparameters: {ldev.FillDAQparameters(adcpar.t4)}")
            print(f"    s_Type:      {adcpar.t4.s_Type}")
            print(f"    FIFO:        {adcpar.t4.FIFO}")
            print(f"    IrqStep:     {adcpar.t4.IrqStep}")
            print(f"    Pages:       {adcpar.t4.Pages}")
            print(f"    AutoInit:    {adcpar.t4.AutoInit}")
            print(f"    dRate:       {adcpar.t4.dRate}")
            print(f"    dKadr:       {adcpar.t4.dKadr}")
            print(f"    Reserved1:   {adcpar.t4.Reserved1}")
            print(f"    DigRate:     {adcpar.t4.DigRate}")
            print(f"    DM_Ena:      {adcpar.t4.DM_Ena}")
            print(f"    Rate:        {adcpar.t4.Rate}")
            print(f"    Kadr:        {adcpar.t4.Kadr}")
            print(f"    StartCnt:    {adcpar.t4.StartCnt}")
            print(f"    StopCnt:     {adcpar.t4.StopCnt}")
            print(f"    SynchroType: {adcpar.t4.SynchroType}")
            print(f"    SynchroMode: {adcpar.t4.SynchroMode}")
            print(f"    AdPorog:     {adcpar.t4.AdPorog}")
            print(f"    SynchroSrc:  {adcpar.t4.SynchroSrc}")
            print(f"    AdcIMask:    {adcpar.t4.AdcIMask}")
            print(f"    NCh:         {adcpar.t4.NCh}")
            # print(f"    Chn:         {list(adcpar.t4.Chn)}")
            print(f"    IrqEna:      {adcpar.t4.IrqEna}")
            print(f"    AdcEna:      {adcpar.t4.AdcEna}")

            data_ptr, syncd = ldev.SetParametersStream(adcpar.t4, buffer_size)
            print(f"SetParametersStream: {data_ptr}, {syncd}")
            print(f"    Pages:   {adcpar.t4.Pages}")
            print(f"    IrqStep: {adcpar.t4.IrqStep}")
            print(f"    FIFO:    {adcpar.t4.FIFO}")
            print(f"    Rate:    {adcpar.t4.dRate}")

        print(f"EnableCorrection: {ldev.EnableCorrection(enable=True)}")

        print(f"InitStartLDevice: {ldev.InitStartLDevice()}")
        print(f"StartLDevice: {ldev.StartLDevice()}")

        print("Read data from buffer ...")

        while syncd() < buffer_size:            # ждем, пока заполнится буфер
            pass

        print("Data ready ...")

        if slpar.BoardType == L_DEVICE.E140:
            x = e140.GetDataADC(adcpar.t3, descr, data_ptr, buffer_size)
        elif slpar.BoardType == L_DEVICE.E440:
            x = e440.GetDataADC(adcpar.t3, descr, data_ptr, buffer_size)
        elif slpar.BoardType == L_DEVICE.E154:
            x = e154.GetDataADC(adcpar.t3, descr, data_ptr, buffer_size)
        elif slpar.BoardType in {L_DEVICE.E2010, L_DEVICE.E2010B}:
            x = e2010.GetDataADC(adcpar.t4, descr, data_ptr, buffer_size)
        elif slpar.BoardType == L_DEVICE.L791:
            x = l791.GetDataADC(adcpar.t4, descr, data_ptr, buffer_size)

        x[0].tofile("channel-1.log", sep="\n")  # индекс соответствует номеру канала из Chn
        # x[1].tofile("channel-2.log", sep="\n")
        # x[2].tofile("channel-3.log", sep="\n")

        print(f"StopLDevice: {ldev.StopLDevice()}")

        # Асинхронные операции ввода/вывода

        asp = WASYNC_PAR()

        asp.s_Type = L_ASYNC.DAC_OUT
        asp.Mode = 0
        asp.Data[0] = 512
        if ldev.IoAsync(asp):
            print(f"IoAsync (L_ASYNC_DAC_OUT): {asp.Data[0]}")

        asp.s_Type = L_ASYNC.ADC_INP
        asp.Chn[0] = 0x00
        if ldev.IoAsync(asp):
            print(f"IoAsync (L_ASYNC_ADC_INP): {asp.Data[0]}")

        asp.s_Type = L_ASYNC.TTL_CFG
        asp.Mode = 1
        if ldev.IoAsync(asp):
            print(f"IoAsync (L_ASYNC_TTL_CFG): {asp.Data[0]}")

        asp.s_Type = L_ASYNC.TTL_INP
        asp.Chn[0] = 0x00
        if ldev.IoAsync(asp):
            print(f"IoAsync (L_ASYNC_TTL_INP): {asp.Data[0]}")

        asp.s_Type = L_ASYNC.TTL_OUT
        asp.Data[0] = 0xA525
        if ldev.IoAsync(asp):
            print(f"IoAsync (L_ASYNC_TTL_OUT): {asp.Data[0]}")

        # Проверка работоспособности других функций

        print(f"SetParameter (L_USER_BASE): {ldev.SetParameter(address=L_USER_BASE, value=123)}")
        print(f"GetParameter (L_USER_BASE): {ldev.GetParameter(address=L_USER_BASE)}")
        print(f"ReadFlashWord: {ldev.ReadFlashWord(address=L_USER_BASE)}")
        print(f"EnableFlashWrite: {ldev.EnableFlashWrite(flag=False)}")
        print(f"SendCommand: {ldev.SendCommand(cmd=0)}")
        print(f"SetLDeviceEvent: {ldev.SetLDeviceEvent(event=0, event_id=L_EVENT.ADC_BUF)}")

        print(f"GetWord_DM: {ldev.GetWord_DM(address=0x0400)}")
        print(f"GetWord_PM: {ldev.GetWord_PM(address=0)}")
        print(f"GetArray_DM: {ldev.GetArray_DM(address=0x1080, count=2)}")
        print(f"GetArray_PM: {ldev.GetArray_PM(address=0, count=2)}")

        print(f"inbyte: {ldev.inbyte(offset=0)}")
        print(f"inword: {ldev.inword(offset=0)}")
        print(f"indword: {ldev.indword(offset=0)}")
        print(f"inmbyte: {ldev.inmbyte(offset=0)}")
        print(f"inmword: {ldev.inmword(offset=0)}")
        print(f"inmdword: {ldev.inmdword(offset=0)}")

        print(f"Get_LDEV2_Interface: {ldev.Get_LDEV2_Interface()}")
        print(f"InitStartLDeviceEx: {ldev.InitStartLDeviceEx(stream_id=L_STREAM.ADC)}")
        print(f"StartLDeviceEx: {ldev.StartLDeviceEx(stream_id=L_STREAM.ADC)}")
        print(f"StopLDeviceEx: {ldev.StopLDeviceEx(stream_id=L_STREAM.ADC)}")
        print(f"Release_LDEV2_Interface: {ldev.Release_LDEV2_Interface()}")
