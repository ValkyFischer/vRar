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
    :param str ext: Optional: Open only this Extension
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
    :param str archiveName: Optional: Set name for rar-archive
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
    :param str configtype: Needs type of config as input
    :return: Returns a list of settings
    """

    # Read config data
    with open(CFG_PATH) as cf:
        cfgData = json.load(cf)

    # Return Lists
    subkeyList = []
    subvalueList = []

    # Step through the json entries
    for key, value in cfgData.items():

        if key == configtype:
            # Check if Logger should be verbose
            if configtype == "debug":
                return value

            subkeyList.append(key)
            subvalueList.append(value)

    # Return settings lists
    return subkeyList, subvalueList


# Log specific messages
def logger(log, message, fileName=None):
    """
    - Creates and writes informations in a log file
    :param int log: 0=DEVICE
    :param str message: Message as string
    :param str fileName: Optional: Filename as string
    """

    # Load types from config
    _, logTypes = config("logger")

    # Check for correct log type
    for logID, logType in logTypes[0].items():
        if logType == log:

            # Set time and date
            dateFile = datetime.today().strftime("%Y%m%d")  # Year first, so its sorted in the directory
            dateLogger = datetime.now().strftime("%Y%m%d-%H:%M:%S")  # Day first, for better readability in logs

            # Log file
            if fileName is None:
                logFile = LOG_PATH + dateFile + "_system.log"
            # Specify Log Filename
            else:
                logFile = LOG_PATH + dateFile + "_" + fileName + ".log"

            # Create log message
            logMessage = dateLogger + " [" + logID + "] " + message + "\n"

            # Check debug mode
            if config("debug"):
                print logMessage.replace("\n", "")  # be verbose

            # Write log
            with open(logFile, "a") as lf:
                lf.write(logMessage)
