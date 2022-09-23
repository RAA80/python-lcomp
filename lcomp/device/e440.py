#! /usr/bin/env python
# -*- coding: utf-8 -*-


cmTEST_E440               = 0
cmENABLE_FLASH_WRITE_E440 = 1
cmREAD_FLASH_WORD_E440    = 2
cmWRITE_FLASH_WORD_E440   = 3
cmSTART_ADC_E440          = 4
cmSTOP_ADC_E440           = 5
cmADC_KADR_E440           = 6
cmADC_SAMPLE_E440         = 7
cmSTART_DAC_E440          = 8
cmSTOP_DAC_E440           = 9
cmDAC_SAMPLE_E440         = 10
cmENABLE_TTL_OUT_E440     = 11
cmTTL_IN_E440             = 12
cmTTL_OUT_E440            = 13
cmLAST_COMMAND_E440       = 14

V_RESET_DSP_E440       = 0
V_PUT_ARRAY_E440       = 1
V_GET_ARRAY_E440       = 2
V_START_ADC_E440       = 3
V_START_DAC_E440       = 4
V_COMMAND_IRQ_E440     = 5
V_GO_SLEEP_E440        = 6
V_WAKEUP_E440          = 7
V_GET_MODULE_NAME_E440 = 11

DM_E440 = 0x4000
PM_E440 = 0x0000


DataBaseAddress_E440 = 0x30

L_PROGRAM_BASE_ADDRESS_E440  = DataBaseAddress_E440 + 0x0
L_READY_E440                 = DataBaseAddress_E440 + 0x1
L_TMODE1_E440                = DataBaseAddress_E440 + 0x2
L_TMODE2_E440                = DataBaseAddress_E440 + 0x3
L_TEST_LOAD_E440             = DataBaseAddress_E440 + 0x4
L_COMMAND_E440               = DataBaseAddress_E440 + 0x5

L_DAC_SCLK_DIV_E440          = DataBaseAddress_E440 + 0x7
L_DAC_RATE_E440              = DataBaseAddress_E440 + 0x8
L_ADC_RATE_E440              = DataBaseAddress_E440 + 0x9
L_ADC_ENABLED_E440           = DataBaseAddress_E440 + 0xA
L_ADC_FIFO_BASE_ADDRESS_E440 = DataBaseAddress_E440 + 0xB
L_CUR_ADC_FIFO_LENGTH_E440   = DataBaseAddress_E440 + 0xC
L_ADC_FIFO_LENGTH_E440       = DataBaseAddress_E440 + 0xE
L_CORRECTION_ENABLED_E440    = DataBaseAddress_E440 + 0xF
L_LBIOS_VERSION_E440         = DataBaseAddress_E440 + 0x10
L_ADC_SAMPLE_E440            = DataBaseAddress_E440 + 0x11
L_ADC_CHANNEL_E440           = DataBaseAddress_E440 + 0x12
L_INPUT_MODE_E440            = DataBaseAddress_E440 + 0x13
L_SYNCHRO_AD_CHANNEL_E440    = DataBaseAddress_E440 + 0x16
L_SYNCHRO_AD_POROG_E440      = DataBaseAddress_E440 + 0x17
L_SYNCHRO_AD_MODE_E440       = DataBaseAddress_E440 + 0x18
L_SYNCHRO_AD_TYPE_E440       = DataBaseAddress_E440 + 0x19

L_CONTROL_TABLE_LENGHT_E440  = DataBaseAddress_E440 + 0x1B
L_FIRST_SAMPLE_DELAY_E440    = DataBaseAddress_E440 + 0x1C
L_INTER_KADR_DELAY_E440      = DataBaseAddress_E440 + 0x1D

L_DAC_SAMPLE_E440            = DataBaseAddress_E440 + 0x20
L_DAC_ENABLED_E440           = DataBaseAddress_E440 + 0x21
L_DAC_FIFO_BASE_ADDRESS_E440 = DataBaseAddress_E440 + 0x22
L_CUR_DAC_FIFO_LENGTH_E440   = DataBaseAddress_E440 + 0x24
L_DAC_FIFO_LENGTH_E440       = DataBaseAddress_E440 + 0x25

L_FLASH_ENABLED_E440         = DataBaseAddress_E440 + 0x26
L_FLASH_ADDRESS_E440         = DataBaseAddress_E440 + 0x27
L_FLASH_DATA_E440            = DataBaseAddress_E440 + 0x28

L_ENABLE_TTL_OUT_E440        = DataBaseAddress_E440 + 0x29
L_TTL_OUT_E440               = DataBaseAddress_E440 + 0x2A
L_TTL_IN_E440                = DataBaseAddress_E440 + 0x2B

L_SCALE_E440                 = DataBaseAddress_E440 + 0x30
L_ZERO_E440                  = DataBaseAddress_E440 + 0x34

L_CONTROL_TABLE_E440         = 0x80
