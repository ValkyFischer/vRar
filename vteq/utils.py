# coding=utf-8

# ---------------------------------------------- #
# Title:            vRar                         #
# Description:      pack and unpack archives     #
# ---------------------------------------------- #
# Author:           fischer@valkyteq.com         #
# Date:             2021-03-27                   #
# Version:          0.0.0001                     #
# Copyright:        VALKYTEQ (c) 2021            #
# ---------------------------------------------- #


# imports
import json
import os
import subprocess
from datetime import datetime


# global variables
CWD = os.getcwd()
RAR_PATH = CWD + "/bin/rar.exe"
CFG_PATH = CWD + "/bin/config.json"
LOG_PATH = CWD + "/logs/"


# unpack rar
def unrar(sourcePath, destinationPath, ext=None):
    """
    - Unpack files from given archive
    :param str sourcePath: Source Archive
    :param str destinationPath: Destination Folder
    :param str ext: Optional: Specify Extension
    :return:
    """

    if ext is not None:
        ext = ext
    else:
        ext = "*.*"

    cmd = subprocess.Popen([RAR_PATH, "x", sourcePath, ext, destinationPath], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    cmdErr, cmdOut = cmd.communicate()

    logger(1, cmdErr)
    logger(1, cmdOut)


# pack rar
def rar(sourcePath, destinationPath, archiveName=None):
    """
    - Pack files from given folder
    :param str sourcePath: Source Archive
    :param str destinationPath: Destination Folder
    :param str archiveName: Optional: Name for rar-archive
    :return:
    """

    if archiveName is not None:
        destinationPath = destinationPath + archiveName + ".rar"
    else:
        destinationPath = destinationPath + ".rar"

    cmd = subprocess.Popen([RAR_PATH, "a", "-r", destinationPath, sourcePath], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    cmdErr, cmdOut = cmd.communicate()

    logger(1, cmdErr)
    logger(1, cmdOut)


# config reader
def config(configtype):
    """
    - Reads settings from config.json
    :param str configtype: Type of config
    :return: Lists of settings
    """

    # Read config data
    with open(CFG_PATH) as cf:
        cfgData = json.load(cf)

    # Return Lists
    keyList = []
    valueList = []

    # Step through the json entries
    for key, value in cfgData.items():

        if key == configtype:
            # Check if Logger should be verbose
            if configtype == "debug":
                return value

            keyList.append(key)
            valueList.append(value)

    # Return settings lists
    return keyList, valueList


# Log specific messages
def logger(log, message, fileName=None):
    """
    - Creates and writes informations in a log file
    :param int log: 0=DEVICE, 1=RAR
    :param str message: Message text
    :param str fileName: Optional: Filename
    """

    # Load types from config
    logTypes = {"VTEQ-DEV-LOG": 0,
                "VTEQ-RAR-LOG": 1}

    # Check for correct log type
    for logType, logID in logTypes.items():
        if logID == log:

            # Set time and date
            dateFile = datetime.today().strftime("%Y%m%d")
            dateLogger = datetime.now().strftime("%Y%m%d-%H:%M:%S")

            # Use correct filename
            if fileName is not None:
                # Specify Log Filename
                logFile = LOG_PATH + dateFile + "_" + fileName + ".log"
            else:
                # Default Log filename
                logFile = LOG_PATH + dateFile + "_system.log"

            # Create log message
            logMessage = dateLogger + " [" + logType + "] " + message

            # Check debug mode
            if config("debug"):
                print logMessage  # be verbose

            # Write log
            with open(logFile, "a") as lf:
                lf.write(logMessage + "\n")
