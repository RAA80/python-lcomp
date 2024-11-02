#ifdef __cplusplus
    #define DllExport(type) extern "C" type
#else
    #define DllExport(type) type
#endif

#include <string.h>
#include <dlfcn.h>

#define INITGUID

#include "../include/stubs.h"
#include "../include/ioctl.h"
#include "../include/ifc_ldev.h"


#define L_ULONG unsigned long long


typedef IDaqLDevice* (*CREATEFUNCPTR)(ULONG slot);


DllExport(HINSTANCE) LoadAPIDLL(char *dllpath)
{
    return (HINSTANCE)dlopen(dllpath, RTLD_LAZY);
}

DllExport(ULONG) FreeAPIDLL(HINSTANCE handle)
{
    return dlclose(handle);
}

DllExport(LPVOID) CallCreateInstance(HINSTANCE hDll, ULONG slot, PULONG Err)
{
    *Err = L_SUCCESS;
    CREATEFUNCPTR CreateInstance = (CREATEFUNCPTR) dlsym(hDll, "CreateInstance");

    char* error = dlerror();
    if(error != NULL)
    {
        *Err = L_ERROR;
        return NULL;
    }

    LUnknown* pIUnknown = CreateInstance(slot);
    if(pIUnknown == NULL)
    {
        *Err = L_ERROR;
        return NULL;
    }

    IDaqLDevice* pI;
    HRESULT hr = pIUnknown->QueryInterface(IID_ILDEV, (void**)&pI);
    if(hr != S_OK)
    {
        *Err = L_ERROR;
        return NULL;
    }

    pIUnknown->Release();

    return pI;
}

// Основные функции

DllExport(HANDLE) OpenLDevice(LPVOID hIfc)
{
    return (HANDLE)(((IDaqLDevice*)hIfc)->OpenLDevice());
}

DllExport(ULONG) CloseLDevice(LPVOID hIfc)
{
    ULONG Err = ((IDaqLDevice*)hIfc)->CloseLDevice();
    ((IDaqLDevice*)hIfc)->Release();

    return Err;
}

DllExport(ULONG) LoadBios(LPVOID hIfc, char *FileName)
{
    return ((IDaqLDevice*)hIfc)->LoadBios(FileName);
}

DllExport(ULONG) PlataTest(LPVOID hIfc)
{
    return ((IDaqLDevice*)hIfc)->PlataTest();
}

DllExport(ULONG) GetSlotParam(LPVOID hIfc, PSLOT_PAR slPar)
{
    return ((IDaqLDevice*)hIfc)->GetSlotParam(slPar);
}

DllExport(ULONG) ReadPlataDescr(LPVOID hIfc, LPVOID pd)
{
    return ((IDaqLDevice*)hIfc)->ReadPlataDescr(pd);
}

DllExport(ULONG) WritePlataDescr(LPVOID hIfc, LPVOID pd, USHORT Ena)
{
    return ((IDaqLDevice*)hIfc)->WritePlataDescr(pd, Ena);
}

DllExport(ULONG) ReadFlashWord(LPVOID hIfc, USHORT FlashAddress, PUSHORT Data)
{
    return ((IDaqLDevice*)hIfc)->ReadFlashWord(FlashAddress, Data);
}

DllExport(ULONG) WriteFlashWord(LPVOID hIfc, USHORT FlashAddress, USHORT Data)
{
    return ((IDaqLDevice*)hIfc)->WriteFlashWord(FlashAddress, Data);
}

DllExport(ULONG) RequestBufferStream(LPVOID hIfc, ULONG *Size, ULONG StreamId)
{
    return ((IDaqLDevice*)hIfc)->RequestBufferStream(Size, StreamId);
}

DllExport(ULONG) FillDAQparameters(LPVOID hIfc, LPVOID sp, ULONG sp_type)
{
    ULONG Err = L_ERROR;
    PWDAQ_PAR wd_sp = (PWDAQ_PAR)sp;

    switch (sp_type)
    {
        case 0:
        {
            DAC_PAR_0 d0_sp;

            d0_sp.s_Type = wd_sp->t1.s_Type;
            d0_sp.FIFO = wd_sp->t1.FIFO;
            d0_sp.IrqStep = wd_sp->t1.IrqStep;
            d0_sp.Pages = wd_sp->t1.Pages;
            d0_sp.AutoInit = wd_sp->t1.AutoInit;
            d0_sp.dRate = wd_sp->t1.dRate;
            d0_sp.Rate = wd_sp->t1.Rate;
            d0_sp.DacNumber = wd_sp->t1.DacNumber;
            d0_sp.DacEna = wd_sp->t1.DacEna;
            d0_sp.IrqEna = wd_sp->t1.IrqEna;

            Err = ((IDaqLDevice*)hIfc)->FillDAQparameters(&d0_sp);
            wd_sp->t1.dRate = d0_sp.dRate;
        } break;
        case 1:
        {
            DAC_PAR_1 d1_sp;

            d1_sp.s_Type = wd_sp->t2.s_Type;
            d1_sp.FIFO = wd_sp->t2.FIFO;
            d1_sp.IrqStep = wd_sp->t2.IrqStep;
            d1_sp.Pages = wd_sp->t2.Pages;
            d1_sp.AutoInit = wd_sp->t2.AutoInit;
            d1_sp.dRate = wd_sp->t2.dRate;
            d1_sp.Rate = wd_sp->t2.Rate;
            d1_sp.DacEna = wd_sp->t2.DacEna;
            d1_sp.IrqEna = wd_sp->t2.IrqEna;

            Err = ((IDaqLDevice*)hIfc)->FillDAQparameters(&d1_sp);
            wd_sp->t2.dRate = d1_sp.dRate;
        } break;
        case 2:
        {
            ADC_PAR_0 a0_sp;

            a0_sp.s_Type = wd_sp->t3.s_Type;
            a0_sp.FIFO = wd_sp->t3.FIFO;
            a0_sp.IrqStep = wd_sp->t3.IrqStep;
            a0_sp.Pages = wd_sp->t3.Pages;
            a0_sp.AutoInit = wd_sp->t3.AutoInit;
            a0_sp.dRate = wd_sp->t3.dRate;
            a0_sp.dKadr = wd_sp->t3.dKadr;
            a0_sp.dScale = wd_sp->t3.dScale;
            a0_sp.Rate = wd_sp->t3.Rate;
            a0_sp.Kadr = wd_sp->t3.Kadr;
            a0_sp.Scale = wd_sp->t3.Scale;
            a0_sp.FPDelay = wd_sp->t3.FPDelay;

            a0_sp.SynchroType = wd_sp->t3.SynchroType;
            a0_sp.SynchroSensitivity = wd_sp->t3.SynchroSensitivity;
            a0_sp.SynchroMode = wd_sp->t3.SynchroMode;
            a0_sp.AdChannel = wd_sp->t3.AdChannel;
            a0_sp.AdPorog = wd_sp->t3.AdPorog;
            a0_sp.NCh = wd_sp->t3.NCh;
            for(int i=0;i<128;i++) a0_sp.Chn[i] = wd_sp->t3.Chn[i];
            a0_sp.AdcEna = wd_sp->t3.AdcEna;
            a0_sp.IrqEna = wd_sp->t3.IrqEna;

            Err = ((IDaqLDevice*)hIfc)->FillDAQparameters(&a0_sp);
            wd_sp->t3.dRate = a0_sp.dRate;
            wd_sp->t3.dKadr = a0_sp.dKadr;
            wd_sp->t3.NCh = a0_sp.NCh;
        } break;
        case 3:
        {
            ADC_PAR_1 a1_sp;

            a1_sp.s_Type = wd_sp->t4.s_Type;
            a1_sp.FIFO = wd_sp->t4.FIFO;
            a1_sp.IrqStep = wd_sp->t4.IrqStep;
            a1_sp.Pages = wd_sp->t4.Pages;
            a1_sp.AutoInit = wd_sp->t4.AutoInit;
            a1_sp.dRate = wd_sp->t4.dRate;
            a1_sp.dKadr = wd_sp->t4.dKadr;
            a1_sp.Reserved1 = wd_sp->t4.Reserved1;
            a1_sp.DigRate = wd_sp->t4.DigRate;
            a1_sp.DM_Ena = wd_sp->t4.DM_Ena;
            a1_sp.Rate = wd_sp->t4.Rate;
            a1_sp.Kadr = wd_sp->t4.Kadr;
            a1_sp.StartCnt = wd_sp->t4.StartCnt;
            a1_sp.StopCnt = wd_sp->t4.StopCnt;

            a1_sp.SynchroType = wd_sp->t4.SynchroType;
            a1_sp.SynchroMode = wd_sp->t4.SynchroMode;
            a1_sp.AdPorog = wd_sp->t4.AdPorog;
            a1_sp.SynchroSrc = wd_sp->t4.SynchroSrc;
            a1_sp.AdcIMask = wd_sp->t4.AdcIMask;
            a1_sp.NCh = wd_sp->t4.NCh;
            for(int i=0;i<128;i++) a1_sp.Chn[i] = wd_sp->t4.Chn[i];
            a1_sp.AdcEna = wd_sp->t4.AdcEna;
            a1_sp.IrqEna = wd_sp->t4.IrqEna;

            Err = ((IDaqLDevice*)hIfc)->FillDAQparameters(&a1_sp);
            wd_sp->t4.dRate = a1_sp.dRate;
            wd_sp->t4.dKadr = a1_sp.dKadr;
            wd_sp->t4.NCh = a1_sp.NCh;
        } break;
    }
    return Err;
}

DllExport(ULONG) SetParametersStream(LPVOID hIfc, LPVOID sp, ULONG sp_type, ULONG *UsedSize, void** Data, void** Sync, ULONG StreamId)
{
    ULONG Err = L_ERROR;
    PWDAQ_PAR wd_sp = (PWDAQ_PAR)sp;

    switch (sp_type)
    {
        case 0:
        {
            DAC_PAR_0 d0_sp;

            Err = ((IDaqLDevice*)hIfc)->SetParametersStream(&d0_sp, UsedSize, (void **)Data, (void **)Sync, StreamId);
            wd_sp->t1.Pages = d0_sp.Pages;
            wd_sp->t1.FIFO = d0_sp.FIFO;
            wd_sp->t1.IrqStep = d0_sp.IrqStep;
        } break;
        case 1:
        {
            DAC_PAR_1 d1_sp;

            Err = ((IDaqLDevice*)hIfc)->SetParametersStream(&d1_sp, UsedSize, (void **)Data, (void **)Sync, StreamId);
            wd_sp->t2.Pages = d1_sp.Pages;
            wd_sp->t2.FIFO = d1_sp.FIFO;
            wd_sp->t2.IrqStep = d1_sp.IrqStep;
        } break;
        case 2:
        {
            ADC_PAR_0 a0_sp;

            Err = ((IDaqLDevice*)hIfc)->SetParametersStream(&a0_sp, UsedSize, (void **)Data, (void **)Sync, StreamId);
            wd_sp->t3.Pages = a0_sp.Pages;
            wd_sp->t3.FIFO = a0_sp.FIFO;
            wd_sp->t3.IrqStep = a0_sp.IrqStep;
            // wd_sp->t3.dRate = a0_sp.dRate;
            // wd_sp->t3.dKadr = a0_sp.dKadr;
        } break;
        case 3:
        {
            ADC_PAR_1 a1_sp;

            Err = ((IDaqLDevice*)hIfc)->SetParametersStream(&a1_sp, UsedSize, (void **)Data, (void **)Sync, StreamId);
            wd_sp->t4.Pages = a1_sp.Pages;
            wd_sp->t4.FIFO = a1_sp.FIFO;
            wd_sp->t4.IrqStep = a1_sp.IrqStep;
            // wd_sp->t4.dRate = a1_sp.dRate;
            // wd_sp->t4.dKadr = a1_sp.dKadr;
        } break;
    }
    return Err;
}

DllExport(ULONG) InitStartLDevice(LPVOID hIfc)
{
    return ((IDaqLDevice*)hIfc)->InitStartLDevice();
}

DllExport(ULONG) StartLDevice(LPVOID hIfc)
{
    return ((IDaqLDevice*)hIfc)->StartLDevice();
}

DllExport(ULONG) StopLDevice(LPVOID hIfc)
{
    return ((IDaqLDevice*)hIfc)->StopLDevice();
}

DllExport(ULONG) EnableCorrection(LPVOID hIfc, USHORT Ena)
{
    return ((IDaqLDevice*)hIfc)->EnableCorrection(Ena);
}

DllExport(ULONG) IoAsync(LPVOID hIfc, PWASYNC_PAR sp)
{
    ASYNC_PAR t_sp;
    ULONG Err;

    t_sp.s_Type = sp->s_Type;

    t_sp.FIFO = sp->FIFO;
    t_sp.IrqStep = sp->IrqStep;
    t_sp.Pages = sp->Pages;

    t_sp.dRate = sp->dRate;
    t_sp.Rate = sp->Rate;
    t_sp.NCh = sp->NCh;
    for(int i=0;i<128;i++) t_sp.Chn[i] = sp->Chn[i];
    for(int j=0;j<128;j++) t_sp.Data[j] = sp->Data[j];
    t_sp.Mode = sp->Mode;

    Err = ((IDaqLDevice*)hIfc)->IoAsync(&t_sp);
    if(Err == L_SUCCESS)
    {
        sp->s_Type = t_sp.s_Type;

        sp->FIFO = t_sp.FIFO;
        sp->IrqStep = t_sp.IrqStep;
        sp->Pages = t_sp.Pages;

        sp->dRate = t_sp.dRate;
        sp->Rate = t_sp.Rate;
        sp->NCh = t_sp.NCh;
        for(int i=0;i<128;i++) sp->Chn[i] = t_sp.Chn[i];
        for(int j=0;j<128;j++) sp->Data[j] = t_sp.Data[j];
        sp->Mode = t_sp.Mode;
    }
    return Err;
}

DllExport(ULONG) GetParameter(LPVOID hIfc, ULONG name, PULONG param)
{
    return ((IDaqLDevice*)hIfc)->GetParameter(name, param);
}

DllExport(ULONG) SetParameter(LPVOID hIfc, ULONG name, PULONG param)
{
    return ((IDaqLDevice*)hIfc)->SetParameter(name, param);
}

DllExport(ULONG) EnableFlashWrite(LPVOID hIfc, USHORT Flag)
{
    return ((IDaqLDevice*)hIfc)->EnableFlashWrite(Flag);
}

DllExport(ULONG) SendCommand(LPVOID hIfc, USHORT Cmd)
{
    return ((IDaqLDevice*)hIfc)->SendCommand(Cmd);
}

DllExport(ULONG) SetLDeviceEvent(LPVOID hIfc, HANDLE hEvent, ULONG EventId)
{
    return ((IDaqLDevice*)hIfc)->SetLDeviceEvent(hEvent, EventId);
}

DllExport(ULONG) GetWord_DM(LPVOID hIfc, USHORT Addr, PUSHORT Data)
{
    return ((IDaqLDevice*)hIfc)->GetWord_DM(Addr, Data);
}

DllExport(ULONG) PutWord_DM(LPVOID hIfc, USHORT Addr, USHORT Data)
{
    return ((IDaqLDevice*)hIfc)->PutWord_DM(Addr, Data);
}

DllExport(ULONG) PutWord_PM(LPVOID hIfc, USHORT Addr, ULONG Data)
{
    return ((IDaqLDevice*)hIfc)->PutWord_PM(Addr, Data);
}

DllExport(ULONG) GetWord_PM(LPVOID hIfc, USHORT Addr, PULONG Data)
{
    return ((IDaqLDevice*)hIfc)->GetWord_PM(Addr, Data);
}

DllExport(ULONG) GetArray_DM(LPVOID hIfc, USHORT Addr, ULONG Count, PUSHORT Data)
{
    return ((IDaqLDevice*)hIfc)->GetArray_DM(Addr, Count, Data);
}

DllExport(ULONG) PutArray_DM(LPVOID hIfc, USHORT Addr, ULONG Count, PUSHORT Data)
{
    return ((IDaqLDevice*)hIfc)->PutArray_DM(Addr, Count, Data);
}

DllExport(ULONG) PutArray_PM(LPVOID hIfc, USHORT Addr, ULONG Count, PULONG Data)
{
    return ((IDaqLDevice*)hIfc)->PutArray_PM(Addr, Count, Data);
}

DllExport(ULONG) GetArray_PM(LPVOID hIfc, USHORT Addr, ULONG Count, PULONG Data)
{
    return ((IDaqLDevice*)hIfc)->GetArray_PM(Addr, Count, Data);
}

// функции для работы с портами ввода/вывода плат

DllExport(ULONG) inbyte(LPVOID hIfc, ULONG offset, PUCHAR data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->inbyte(offset, data, len, key);
}

DllExport(ULONG) inword(LPVOID hIfc, ULONG offset, PUSHORT data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->inword(offset, data, len, key);
}

DllExport(ULONG) indword(LPVOID hIfc, ULONG offset, PULONG data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->indword(offset, data, len, key);
}

DllExport(ULONG) outbyte(LPVOID hIfc, ULONG offset, PUCHAR data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outbyte(offset, data, len, key);
}

DllExport(ULONG) outword(LPVOID hIfc, ULONG offset, PUSHORT data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outword(offset, data, len, key);
}

DllExport(ULONG) outdword(LPVOID hIfc, ULONG offset, PULONG data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outdword(offset, data, len, key);
}

DllExport(ULONG) inmbyte(LPVOID hIfc, ULONG offset, PUCHAR data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->inmbyte(offset, data, len, key);
}

DllExport(ULONG) inmword(LPVOID hIfc, ULONG offset, PUSHORT data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->inmword(offset, data, len, key);
}

DllExport(ULONG) inmdword(LPVOID hIfc, ULONG offset, PULONG data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->inmdword(offset, data, len, key);
}

DllExport(ULONG) outmbyte(LPVOID hIfc, ULONG offset, PUCHAR data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outmbyte(offset, data, len, key);
}

DllExport(ULONG) outmword(LPVOID hIfc, ULONG offset, PUSHORT data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outmword(offset, data, len, key);
}

DllExport(ULONG) outmdword(LPVOID hIfc, ULONG offset, PULONG data, ULONG len, ULONG key)
{
    return ((IDaqLDevice*)hIfc)->outmdword(offset, data, len, key);
}

// Для LabView

DllExport(ULONG) GetSyncData(LPVOID hIfc, L_ULONG SyncPtr, ULONG Offset, ULONG *Sync)
{
    *Sync = *((PULONG)SyncPtr);
    return 0;
}

DllExport(ULONG) GetDataFromBuffer(LPVOID hIfc, L_ULONG DataPtr, LPVOID DataArray, ULONG size, ULONG mask)
{
    UCHAR *D;
    D = (PUCHAR)DataArray;
    for(ULONG j=0; j<size; j++) D[j] = ((PUCHAR)DataPtr)[j];

    ULONG *DA;
    DA = (PULONG)DataArray;
    if(mask)
        for(ULONG i=0; i<size/sizeof(ULONG); i++) DA[i] = DA[i] & mask;

    return 0;
}

DllExport(ULONG) PutDataToBuffer(LPVOID hIfc, L_ULONG DataPtr, LPVOID DataArray, ULONG size)
{
    memcpy((LPVOID)DataPtr, DataArray, size*sizeof(UCHAR));
    return 0;
}

// Расширенный интерфейс для работы с устройствами

DllExport(LPVOID) Get_LDEV2_Interface(LPVOID hIfc, PULONG Err)
{
    *Err = L_NOTSUPPORTED;
    return NULL;
}

DllExport(ULONG) Release_LDEV2_Interface(LPVOID hIfc)
{
    return L_NOTSUPPORTED;
}

DllExport(ULONG) InitStartLDeviceEx(LPVOID hIfc, ULONG StreamId)
{
    return L_NOTSUPPORTED;
}

DllExport(ULONG) StartLDeviceEx(LPVOID hIfc, ULONG StreamId)
{
    return L_NOTSUPPORTED;
}

DllExport(ULONG) StopLDeviceEx(LPVOID hIfc, ULONG StreamId)
{
    return L_NOTSUPPORTED;
}
