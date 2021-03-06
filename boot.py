# coding=utf-8

# ---------------------------------------------- #
# Title:            VRAR                         #
# Description:      pack and unpack archives     #
# ---------------------------------------------- #
# Author:           fischer@valkyteq.com         #
# Date:             2021-03-28                   #
# Version:          1.0.0001                     #
# Copyright:        VALKYTEQ (c) 2021            #
# ---------------------------------------------- #


# imports
from vteq import utils, control
from sched import scheduler
from time import time, sleep


# Timer
TIMER = scheduler(time, sleep)


# Load settings from config
_, settings = utils.config("settings")
for setting, value in settings[0].items():
    if setting == "interval":
        TIMER_INTERVAL = value * 60  # interval in config is in minutes
        TIMER_PRIO = 1


# Start Scheduler
def vrarScheduler(schedule):
    """
    - Looping function to run itself based on a given timer
    - TIMER_INTERVAL gets applied *after* VRAR controller ran through
    :param object schedule: Needs built in "sched" as input
    """

    control.control()
    utils.logger(0, "*" * 70)

    # Run itself (and start scheduler)
    TIMER.enter(TIMER_INTERVAL, TIMER_PRIO, vrarScheduler, (schedule,))


# Startup
def startup():
    """
    - Loads VRAR Version Information
    - Starts VRAR Scheduler
    """

    """
    **********************************************************************
         __    __  __     _      _   __ __  __
         \ \  / / /  \   | |    | |_/ / \ \/ /
          \ \/ / / __ \  | |__  |  __ \  \  /
           \__/ /_/  \_\ |____| |_|  \_\ /_/
    
    **********************************************************************
    """

    # Startup Strings
    strLine =    "*" * 70
    strTitle =   "VRAR - VALKYTEQ Rar Archive Resolution"
    strAuthor =  "Author    :  fischer@valkyteq.com"
    strDate =    "Date      :  2021-03-28"
    strVersion = "Version   :  v0.0.0001"
    strCright =  "Copyright :  VALKYTEQ (c) 2021"
    startupLog = [strLine, strTitle, strLine, strAuthor, strDate, strVersion, strCright, strLine]

    # Write logs
    for line in startupLog:
        utils.logger(0, line)

    # Check if Debug Mode is enabled
    if utils.config("debug"):
        utils.logger(0, "Debug Mode enabled: VERBOSE")

    # Write log
    utils.logger(0, "Starting VRAR Scheduler, Timer Delay: {delay}s Priority: {prio}".format(delay=TIMER_INTERVAL, prio=TIMER_PRIO))
    # Start and enter Interval Timer
    TIMER.enter(10, TIMER_PRIO, vrarScheduler, (TIMER,))
    TIMER.run()
