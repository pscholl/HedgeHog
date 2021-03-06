/********************************************************************
 FileName:     	BMA150.h,     the BMA150 lib header file
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef BMA150__H
#define BMA150__H

#include "Compiler.h"
#include "GenericTypeDefs.h"
#include "HardwareProfile.h"
#include "HHG_conf.h"       // for acc configuration
#include "acc3D_wrapper.h"

#define BMA150_ADDR15 0x15
#define BMA150_ADDR14 0x14
#define BMA150_ADDR13 0x13
#define BMA150_ADDR12 0x12
#define BMA150_ADDR11 0x11
#define BMA150_ADDR10 0x10
#define BMA150_ADDR0F 0x0F
#define BMA150_ADDR0E 0x0E
#define BMA150_ADDR0D 0x0D
#define BMA150_ADDR0C 0x0C
#define BMA150_ADDR0B 0x0B
#define BMA150_ADDR0A 0x0A
#define BMA150_ADDR09 0x09

#define BMA150_TEMP 0x08

#define BMA150_ACC_Z_MSB 0x07
#define BMA150_ACC_Z_LSB 0x06
#define BMA150_ACC_Y_MSB 0x05
#define BMA150_ACC_Y_LSB 0x04
#define BMA150_ACC_X_MSB 0x03
#define BMA150_ACC_X_LSB 0x02
#define BMA150_VERSION 0x01
#define BMA150_CHIP_ID 0x00

#define BMA150_READ 0x80
#define BMA150_WRITE 0x00

#define BMA150_RANGE_2G 0
#define BMA150_RANGE_4G 1
#define BMA150_RANGE_8G 2

#define BMA150_BW_25 0x00
#define BMA150_BW_50 0x01
#define BMA150_BW_100 0x02
#define BMA150_BW_190 0x03
#define BMA150_BW_375 0x04
#define BMA150_BW_750 0x05
#define BMA150_BW_1500 0x06

typedef union
{
    //Address 0x00
    struct
    {
        BYTE chip_id :3;
        BYTE :5;
    } ;
    //Address 0x01
    struct
    {
        BYTE ml_version :4;
        BYTE al_version :4;
    } ;
    //Address 0x02
    struct
    {
        BYTE new_data_x :1;
        BYTE :5;
        BYTE acc_x :2;
    } ;
    //Address 0x03
    struct
    {
        BYTE acc_x :8;
    } ;
    //Address 0x04
    struct
    {
        BYTE new_data_y :1;
        BYTE :5;
        BYTE acc_y :2;
    } ;
    //Address 0x05
    struct
    {
        BYTE acc_y :8;
    } ;
    //Address 0x06
    struct
    {
        BYTE new_data_z :1;
        BYTE :5;
        BYTE acc_z :2;
    } ;
    //Address 0x07
    struct
    {
        BYTE acc_z :8;
    } ;
    //Address 0x14
    struct
    {
        BYTE bandwidth :3;  
        BYTE range :2;
		BYTE :3;
    } ;
    BYTE val;
} BMA150_REG;

#define bma150_get_tmp() (bma150_read_byte(BMA150_TEMP))

void bma150_init(hhg_conf_accs_t cnf, UINT32_VAL* initmsg);
void bma150_SPI_init(void);
void bma150_getXYZ(PACC_XYZ);
void bma150_write_byte(BYTE address, BYTE data);
BYTE bma150_read_byte(BYTE address);
void bma150_set_conf(BYTE range, BYTE bw);
void bma150_write_str(PACC_XYZ bma150_xyz, char* acc_buff);

#endif // BMA150__H