#!/usr/bin/env python

# script to format SD command log csv files

import csv
import sys
import argparse

NAME = 0
DESCRIPTION = 1

READ = 0
WRITE = 1

mmc_commands = {
    0: "MMC_CMD_GO_IDLE_STATE",
    1: "MMC_CMD_SEND_OP_COND",
    2: "MMC_CMD_ALL_SEND_CID",
    3: "MMC_CMD_SET_RELATIVE_ADDR",
    4: "MMC_CMD_SET_DSR",
    6: "MMC_CMD_SWITCH",
    7: "MMC_CMD_SELECT_CARD",
    8: "MMC_CMD_SEND_EXT_CSD",
    9: "MMC_CMD_SEND_CSD",
    10: "MMC_CMD_SEND_CID",
    12: "MMC_CMD_STOP_TRANSMISSION",
    13: "MMC_CMD_SEND_STATUS",
    16: "MMC_CMD_SET_BLOCKLEN",
    17: "MMC_CMD_READ_SINGLE_BLOCK",
    18: "MMC_CMD_READ_MULTIPLE_BLOCK",
    19: "MMC_CMD_SEND_TUNING_BLOCK",
    21: "MMC_CMD_SEND_TUNING_BLOCK_HS200",
    23: "MMC_CMD_SET_BLOCK_COUNT        ",
    24: "MMC_CMD_WRITE_SINGLE_BLOCK",
    25: "MMC_CMD_WRITE_MULTIPLE_BLOCK",
    35: "MMC_CMD_ERASE_GROUP_START",
    36: "MMC_CMD_ERASE_GROUP_END",
    38: "MMC_CMD_ERASE",
    55: "MMC_CMD_APP_CMD",
    58: "MMC_CMD_SPI_READ_OCR",
    59: "MMC_CMD_SPI_CRC_ON_OFF",
    62: "MMC_CMD_RES_MAN",
    3: "SD_CMD_SEND_RELATIVE_ADDR",
    6: "SD_CMD_SWITCH_FUNC",
    8: "SD_CMD_SEND_IF_COND",
    11: "SD_CMD_SWITCH_UHS18V",
    6: "SD_CMD_APP_SET_BUS_WIDTH",
    13: "SD_CMD_APP_SD_STATUS",
    32: "SD_CMD_ERASE_WR_BLK_START",
    33: "SD_CMD_ERASE_WR_BLK_END",
    41: "SD_CMD_APP_SEND_OP_COND",
    51: "SD_CMD_APP_SEND_SCR",
}

MMC_RSP_PRESENT = (1 << 0)
MMC_RSP_136 = (1 << 1)
MMC_RSP_CRC = (1 << 2)
MMC_RSP_BUSY = (1 << 3)
MMC_RSP_OPCODE = (1 << 4)

MMC_RSP_NONE = 0
MMC_RSP_R1 = (MMC_RSP_PRESENT | MMC_RSP_CRC | MMC_RSP_OPCODE)
MMC_RSP_R1b = (MMC_RSP_PRESENT | MMC_RSP_CRC | MMC_RSP_OPCODE | MMC_RSP_BUSY)
MMC_RSP_R2 = (MMC_RSP_PRESENT | MMC_RSP_136 | MMC_RSP_CRC)
MMC_RSP_R3 = (MMC_RSP_PRESENT)
MMC_RSP_R4 = (MMC_RSP_PRESENT)
MMC_RSP_R5 = (MMC_RSP_PRESENT | MMC_RSP_CRC | MMC_RSP_OPCODE)
MMC_RSP_R6 = (MMC_RSP_PRESENT | MMC_RSP_CRC | MMC_RSP_OPCODE)
MMC_RSP_R7 = (MMC_RSP_PRESENT | MMC_RSP_CRC | MMC_RSP_OPCODE)

mmc_responses = {
        MMC_RSP_NONE: "MMC_RSP_NONE",
        MMC_RSP_R1: "MMC_RSP_R1",
        MMC_RSP_R1b: "MMC_RSP_R1b",
        MMC_RSP_R2: "MMC_RSP_R2",
        MMC_RSP_R3: "MMC_RSP_R3",
        MMC_RSP_R4: "MMC_RSP_R4",
        MMC_RSP_R5: "MMC_RSP_R5",
        MMC_RSP_R6: "MMC_RSP_R6",
        MMC_RSP_R7: "MMC_RSP_R7",
        }

def main():
    parser = argparse.ArgumentParser(description='Parse SD command logs and format them')
    parser.add_argument('--header', action="store_true", default=False, help="Print header line")
    parser.add_argument('file', action="store")
    args = parser.parse_args()
    if args.header:
        print("")
    start_timestamp = -1
    rows = []
    with open(args.file) as csvfile:
        register_log_reader = csv.reader(csvfile, delimiter=',')
        for row in register_log_reader:
            rows.append(row)
    for index, row in enumerate(rows):
        #print(row)
        _, command_dec, arg_hex, response_type_dec = row
        command = int(command_dec)
        arg = int(arg_hex, 16)
        response_type = 0
        if response_type_dec:
            response_type = int(response_type_dec)
        command_name = mmc_commands.get(command, "UNKNOWN")
        response_name = mmc_responses.get(response_type, "UNKNOWN")
        print(f"{index:3d} {command: >5} {arg:#010x}:   {command_name: <30}  {response_name}")


if __name__ == "__main__":
    main()
