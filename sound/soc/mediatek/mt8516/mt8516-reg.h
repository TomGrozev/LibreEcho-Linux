/* SPDX-License-Identifier: GPL-2.0 */
/*
 * MediaTek MT8516 audio front end register definitions
 *
 * Copyright (c) 2016 MediaTek Inc.
 *
 * Derived from the MediaTek/Amazon mt8167 driver in Amazon's GPL release.
 */

#ifndef _MT8516_REG_H_
#define _MT8516_REG_H_

#include <linux/bits.h>

#define AUDIO_TOP_CON0			0x0000
#define AFE_DAC_CON0			0x0010
#define AFE_DAC_CON1			0x0014
#define AFE_CONN1			0x0024
#define AFE_CONN2			0x0028
#define AFE_I2S_CON1			0x0034
#define AFE_I2S_CON2			0x0038
#define AFE_DL1_BASE			0x0040
#define AFE_DL1_CUR			0x0044
#define AFE_DL1_END			0x0048
#define AFE_CONN_24BIT			0x006c
#define AFE_AWB_BASE			0x0070
#define AFE_AWB_END			0x0078
#define AFE_AWB_CUR			0x007c
#define AFE_ADDA_TOP_CON0		0x0120
#define AFE_CONN_TDMIN_CON		0x039c
#define AFE_IRQ_MCU_CON			0x03a0
#define AFE_IRQ_STATUS			0x03a4
#define AFE_IRQ_CLR			0x03a8
#define AFE_IRQ_CNT1			0x03ac
#define AFE_IRQ_MCU_EN			0x03b4
#define AFE_MEMIF_PBUF_SIZE		0x03d8
#define AFE_IRQ_CNT7			0x03dc
#define AFE_MEMIF_PBUF2_SIZE		0x03ec
#define AFE_APLL1_TUNER_CFG		0x03f0
#define AFE_APLL2_TUNER_CFG		0x03f4
#define AFE_IRQ_MCU_CON2		0x03f8
#define AFE_TDM_IN_CON1			0x0588
#define AFE_IRQ_CNT10			0x08dc
#define AFE_HDMI_IN_2CH_CON0		0x09c0
#define AFE_HDMI_IN_2CH_BASE		0x09c4
#define AFE_HDMI_IN_2CH_END		0x09c8
#define AFE_HDMI_IN_2CH_CUR		0x09cc
#define ABB_AFE_SDM_TEST		0x0f4c

#define AFE_MAX_REGISTER		ABB_AFE_SDM_TEST

/* AUDIO_TOP_CON0 */
#define AUD_TCON0_PDN_APLL_TUNER	BIT(19)
#define AUD_TCON0_PDN_APLL2_TUNER	BIT(18)
#define AUD_TCON0_PDN_24M		BIT(9)
#define AUD_TCON0_PDN_22M		BIT(8)
#define AUD_TCON0_PDN_AFE		BIT(2)

/* AFE_DAC_CON0 */
#define AFE_DAC_CON0_AFE_ON		BIT(0)

/* AFE_I2S_CON1: I2S output feeding the I2S_8CH pads */
#define AFE_I2S_CON1_I2S2_TO_PAD	BIT(18)
#define AFE_I2S_CON1_LOW_JITTER_CLK	BIT(12)
#define AFE_I2S_CON1_RATE_MASK		GENMASK(11, 8)
#define AFE_I2S_CON1_FORMAT_I2S		BIT(3)
#define AFE_I2S_CON1_WLEN_32BIT		BIT(1)
#define AFE_I2S_CON1_EN			BIT(0)

/* AFE_I2S_CON2: I2S input sharing its clocks with the I2S output */
#define AFE_I2S_CON2_UPDATE_WORD	GENMASK(28, 24)
#define AFE_I2S_CON2_LOW_JITTER_CLK	BIT(12)
#define AFE_I2S_CON2_RATE_MASK		GENMASK(11, 8)
#define AFE_I2S_CON2_FORMAT_I2S		BIT(3)
#define AFE_I2S_CON2_WLEN_32BIT		BIT(1)
#define AFE_I2S_CON2_EN			BIT(0)

/* AFE_CONN1/AFE_CONN2: interconnect switches, input Ixx to output Oxx */
#define AFE_CONN1_I05_O03_S		21
#define AFE_CONN2_I06_O04_S		6
#define AFE_CONN2_I05_O05_S		19
#define AFE_CONN2_I06_O06_S		24

/* AFE_CONN_24BIT */
#define AFE_CONN_24BIT_O06		BIT(6)
#define AFE_CONN_24BIT_O05		BIT(5)
#define AFE_CONN_24BIT_O04		BIT(4)
#define AFE_CONN_24BIT_O03		BIT(3)

/* AFE_ADDA_TOP_CON0 */
#define AFE_ADDA_TOP_CON0_EXT_ADC	BIT(0)

/* AFE_CONN_TDMIN_CON */
#define AFE_CONN_TDMIN_O41_I41		(0x1 << 3)
#define AFE_CONN_TDMIN_O40_I40		(0x0 << 0)
#define AFE_CONN_TDMIN_CON0_MASK	GENMASK(5, 0)

/* AFE_IRQ_STATUS / AFE_IRQ_CLR */
#define AFE_IRQ_STATUS_BITS		GENMASK(14, 0)

/* AFE_IRQ_MCU_EN */
#define AFE_IRQ_MCU_EN_ALL		GENMASK(7, 0)

/* AFE_APLLx_TUNER_CFG */
#define AFE_APLL_TUNER_CFG_MASK		GENMASK(15, 1)
#define AFE_APLL_TUNER_CFG_EN		BIT(0)
#define AFE_APLL1_TUNER_CFG_VAL		0x832
#define AFE_APLL2_TUNER_CFG_VAL		0x634

/* AFE_TDM_IN_CON1 */
#define AFE_TDM_IN_CON1_LRCK_WIDTH(x)		(((x) - 1) << 24)
#define AFE_TDM_IN_CON1_DISABLE_CH67		BIT(19)
#define AFE_TDM_IN_CON1_FAST_LRCK_CYCLE_32BCK	(0x2 << 12)
#define AFE_TDM_IN_CON1_FAST_LRCK_CYCLE_16BCK	(0x0 << 12)
#define AFE_TDM_IN_CON1_8CH_PER_SDATA		(0x2 << 10)
#define AFE_TDM_IN_CON1_4CH_PER_SDATA		(0x1 << 10)
#define AFE_TDM_IN_CON1_2CH_PER_SDATA		(0x0 << 10)
#define AFE_TDM_IN_CON1_WLEN_32BIT		(0x3 << 8)
#define AFE_TDM_IN_CON1_WLEN_16BIT		(0x1 << 8)
#define AFE_TDM_IN_CON1_I2S			BIT(3)
#define AFE_TDM_IN_CON1_LRCK_INV		BIT(2)
#define AFE_TDM_IN_CON1_BCK_INV			BIT(1)
#define AFE_TDM_IN_CON1_EN			BIT(0)

#endif
