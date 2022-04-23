#! /usr/bin/env python
# -*- coding: utf-8 -*-


V_RESET_DSP_E154       = 0
V_PUT_ARRAY_E154       = 1
V_GET_ARRAY_E154       = 2
V_START_ADC_E154       = 3
V_STOP_ADC_E154        = 4
V_START_ADC_ONCE_E154  = 5
V_GET_MODULE_NAME_E154 = 11

L_ADC_PARS_BASE_E154      = 0x0060
L_ADC_ONCE_FLAG_E154      = L_ADC_PARS_BASE_E154 + 136
L_FLASH_ENABLED_E154      = L_ADC_PARS_BASE_E154 + 137
L_TTL_OUT_E154            = 0x0400
L_TTL_IN_E154             = 0x0400
L_ENABLE_TTL_OUT_E154     = 0x0402
L_ADC_SAMPLE_E154         = 0x0410
L_ADC_CHANNEL_SELECT_E154 = 0x0412
L_ADC_START_E154          = 0x0413
L_DAC_SAMPLE_E154         = 0x0420
L_SUSPEND_MODE_E154       = 0x0430
L_DATA_FLASH_BASE_E154    = 0x0800
L_CODE_FLASH_BASE_E154    = 0x1000
L_BIOS_VERSION_E154       = 0x1080
L_DESCRIPTOR_BASE_E154    = 0x2780
L_RAM_E154                = 0x8000
