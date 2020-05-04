#!/usr/bin/env python

# script to format register log csv files

import csv
import sys
import argparse

NAME = 0
DESCRIPTION = 1

READ = 0
WRITE = 1

registers = {
        0x0000: ["DSADDR", "DMA System Address Register"],
        0x0004: ["BLKATTR", "Block Attributes Register"],
        0x0008: ["CMDARG", "Command Argument Register"],
        0x000c: ["XFERTYP", "Transfer Type Register SAMA5: Transfer Mode Register"],
        0x0010: ["CMDRSP0", "Command Response 0"],
        0x0014: ["CMDRSP1", "Command Response 1"],
        0x0018: ["CMDRSP2", "Command Response 2"],
        0x001c: ["CMDRSP3", "Command Response 3"],
        0x0020: ["DATAPORT", "Buffer Data Port Register"],
        0x0024: ["PRSSTAT", "Present State Register"],
        0x0028: ["PROCTL", "Protocol Control Register"],
        0x002c: ["SYSCTL", "System Control Register, or Clock Control Register/Timout Control Register"],
        0x0030: ["IRQSTAT", "Interrupt Status Register"],
        0x0034: ["IRQSTATEN", "Interrupt Status Enable Register"],
        0x0038: ["IRQSIGEN", "Interrupt Signal Enable Register"],
        0x003c: ["AC12ERR", "Auto CMD12 Error Status Register"],
        0x0040: ["HTCAPBLT0", "Host Controller Capabilities 0 Register"],
        0x0044: ["HTCAPBLT1", "Host Controller Capabilities 1 Register"],
        0x0048: ["MIX", "Mixer Control Register SAMA5: Maximum Current Capabililities Register"],
        0x0050: ["FEVT", "Force Event Register"],
        0x0054: ["ADMAES", "ADMA Error Status Register"],
        0x0058: ["ADSADDR", "ADMA System Address Register"],
        0x0060: ["DLL_CONTROL", "DLL Control Register"],
        0x0064: ["DLL_STATUS", "DLL Status Register"],
        0x0068: ["CLK_TUNE_CTRL", "Clock tuning control Register"],
        0x00fe: ["HOST_VERSION", "Host Controller Version Register"],
        0x0200: ["APSR", "Additional Present State Register"],
        0x0204: ["MC1R", "e.MMC Control 1 Register"],
        0x0205: ["MC2R", "e.MMC Control 2 Register"],
        0x0208: ["ACR", "AHB Control Register"],
        0x020C: ["CC2R", "Clock Control 2 Register"],
        0x0210: ["RTC1R", "Retuning Timer Control 1 Register"],
        0x0211: ["RTC2R", "Retuning Timer Control 2 Register"],
        0x0214: ["RTCVR", "Retuning Timer Counter Value Register"],
        0x0218: ["RTISTER", "Retuning Timer Interrupt Status Enable Register"],
        0x0219: ["RTISIER", "Retuning Timer Interrupt Signal Enable Register"],
        0x021C: ["RTISTR", "Retuning Timer Interrupt Status Register"],
        0x021D: ["RTSSR", "Retuning Timer Status Slots Register"],
        0x0220: ["TUNCR", "Tuning Control Register"],
        0x0230: ["CACR", "Capabilities Control Register"],
        0x0240: ["CALCR", "Calibration Control Register"],

        # Atmel
        0x0006: ["BCR", "Block Count Register"],
        0x000e: ["CR", "Command Register"],
        0x0013: ["RR0", "Response Register 0 (upper byte)"],
        0x0017: ["RR1", "Response Register 1 (upper byte)"],
        0x001b: ["RR3", "Response Register 3 (upper byte)"],
        0x0029: ["PCR", "Power Control Register"],
        0x002e: ["TCR", "Timeout Control Register"],
        0x002f: ["SRR", "Software Reset Register"],
}


def main():
    parser = argparse.ArgumentParser(description='Parse SDMMC register logs and format them')
    parser.add_argument('--description', action="store_true", default=False, help="Print register long descriptions")
    parser.add_argument('--header', action="store_true", default=False, help="Print header line")
    parser.add_argument('--c-format', action="store_true", default=False, help="Output C-language data structure")
    parser.add_argument('file', action="store")
    args = parser.parse_args()
    if args.header:
        print("index   usecs  op (bytes) register               value         value binary                             register long description")
    start_timestamp = -1
    rows = []
    with open(args.file) as csvfile:
        register_log_reader = csv.reader(csvfile, delimiter=',')
        for row in register_log_reader:
            rows.append(row)
    if args.c_format:
        print("/* register log format: usecs, read/write, bytes, register, value */")
        print(f"int REGISTER_LOG_LENGTH = {len(rows)};")
        print(f"register_log[{len(rows)}][5] = {{")
    for index, row in enumerate(rows):
        # print(row)
        prefix, operation, bytes_hex, timestamp_dec, register_address, register_hex, value_hex = row
        if operation == "write":
            op = 'w'
            opcode = WRITE
        else:
            op = ' '
            opcode = READ
        timestamp = int(timestamp_dec)
        if start_timestamp < 0:
            start_timestamp = timestamp
        bytes = int(bytes_hex)
        register = int(register_hex, 16)
        if value_hex:
            value = int(value_hex, 16)
        if register in registers:
            reg_name = registers[register][NAME]
            reg_description = registers[register][DESCRIPTION]
        else:
            reg_name = "UNKNOWN"
            reg_description = "Unknown register"
        display_timestamp = timestamp - start_timestamp
        if args.c_format:
            print(f"{display_timestamp:10d}, {opcode}, {bytes}, {register:#06x}, {value:#010x},  /* {reg_name} - {reg_description}  */ ")
        else:
            print(f"{index:3d} {display_timestamp:10d} {operation: >5} ({bytes}): [{register:#06x}:{reg_name: >12}]{op} ", end='')
            if value_hex:
                vb = f'{value:>032b}'
                value_binary = f'{vb[0:4]} {vb[4:8]} {vb[8:12]} {vb[12:16]} {vb[16:20]} {vb[20:24]} {vb[24:28]} {vb[28:32]}'
                print(f"{value:#010x}    {value_binary}", end='')
            else:
                print("                                                     ", end='')
            if args.description:
                print(f"  {reg_description}", end='')
            print()
    if args.c_format:
        print("}")


if __name__ == "__main__":
    main()
