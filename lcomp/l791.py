#! /usr/bin/env python
# -*- coding: utf-8 -*-


# raw L791 registers
R_ADC_BUFFER_L791           = 0x000
R_DAC_BUFFER_L791           = 0x400
R_CONTROL_TABLE_L791        = 0x600
R_CONTROL_TABLE_LENGTH_L791 = 0x7F4
R_CHANNEL_TIME_L791         = 0x7F8
R_INT_FRAME_TIME_L791       = 0x7FC
R_ADC_PAGE_DESC_L791        = 0x800
R_DAC_PAGE_DESC_L791        = 0xA00
R_ADC_PCI_COUNT_L791        = 0xF80
R_DAC_PCI_COUNT_L791        = 0xF84
R_DAC_TIME_L791             = 0xF88
R_ADC_BUFFER_PTR_L791       = 0xF90
R_DAC_BUFFER_PTR_L791       = 0xF94
R_DIGITAL_IO_L791           = 0xF98
R_ADC_SAMPLE_QNT_L791       = 0xF9C
R_ADC_MASTER_QNT_L791       = 0xFA0
R_FLASH_ADDRESS_L791        = 0xFA4
R_FLASH_DATA_L791           = 0xF8C
R_INTERRUPT_ENABLE_L791     = 0xFF0
R_STATUS_L791               = 0xFF8
R_CONTROL_L791              = 0xFFC

# dword array access index
I_ADC_BUFFER_L791           = 0x000 >> 2
I_DAC_BUFFER_L791           = 0x400 >> 2
I_CONTROL_TABLE_L791        = 0x600 >> 2
I_CONTROL_TABLE_LENGTH_L791 = 0x7F4 >> 2
I_CHANNEL_TIME_L791         = 0x7F8 >> 2
I_INT_FRAME_TIME_L791       = 0x7FC >> 2
I_ADC_PAGE_DESC_L791        = 0x800 >> 2
I_DAC_PAGE_DESC_L791        = 0xA00 >> 2
I_ADC_PCI_COUNT_L791        = 0xF80 >> 2
I_DAC_PCI_COUNT_L791        = 0xF84 >> 2
I_DAC_TIME_L791             = 0xF88 >> 2
I_ADC_BUFFER_PTR_L791       = 0xF90 >> 2
I_DAC_BUFFEI_PTR_L791       = 0xF94 >> 2
I_DIGITAL_IO_L791           = 0xF98 >> 2
I_ADC_SAMPLE_QNT_L791       = 0xF9C >> 2
I_ADC_MASTER_QNT_L791       = 0xFA0 >> 2
I_FLASH_ADDRESS_L791        = 0xFA4 >> 2
I_FLASH_DATA_L791           = 0xF8C >> 2
I_INTERRUPT_ENABLE_L791     = 0xFF0 >> 2
I_STATUS_L791               = 0xFF8 >> 2
I_CONTROL_L791              = 0xFFC >> 2

# bits defines
# CONTROL_REGISTER
BIT_ADC_EN            = 0
BIT_ADC_MASTER_EN     = 1
BIT_CLR_ADC_CNT       = 2
BIT_AUTO_STOP_ADC_MST = 3
BIT_AUTO_STOP_ADC     = 4
# 5-7 reserved
BIT_SYNC_MODE_0       = 8
BIT_SYNC_MODE_1       = 9
BIT_SYNC_SOURCE       = 10
# 11 reserved
BIT_ADC_BUF_DEPTH_0   = 12
BIT_ADC_BUF_DEPTH_1   = 13
BIT_ADC_BUF_DEPTH_2   = 14
# 15 reserved
BIT_DAC_EN            = 16
BIT_DAC_MASTER_EN     = 17
BIT_CLR_DAC_CNT       = 18
# 19-23 reserved
BIT_EEPROM_CMD_0      = 24
BIT_EEPROM_CMD_1      = 25
BIT_EEPROM_START      = 26
BIT_EEPROM_WR_EN      = 27
BIT_OUTPUT_EN         = 28
# 29-31 reserved

# STATUS_REGISTER
SBIT_ADC_MST_EVENT = 0
SBIT_ADC_OVF_EVENT = 1
# 2 reserved
SBIT_ADC_BUF_EVENT = 3
# 4-15 reserved
SBIT_DAC_USR_EVENT = 16
# 17 reserved
SBIT_DAC_UNF_EVENT = 18
# 19-23 reserved
SBIT_PWR_OVR_EVENT = 24
SBIT_EEPROM_BUSY   = 25
# 26 -30 reserved
SBIT_INT           = 31
