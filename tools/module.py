import aiomysql
import asyncio
import traceback
import logging
import os
import sys
import json

#######################################
# Expection function
#######################################

def exceptions(e, level=logging.ERROR, log_file=None):
    logger = logging.getLogger(__name__)
    e_type, e_object, e_traceback = sys.exc_info()
    e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
    e_message = str(e)
    e_line_number = e_traceback.tb_lineno
    log_message = "\n---------------------------------------------------------------------------------------------\n"
    log_message += "---------------------------------------------------------------------------------------------\n"
    log_message += f"Exception type: {e_type}\n"
    log_message += f"Exception filename: {e_filename}\n"
    log_message += f"Exception line number: {e_line_number}\n"
    log_message += f"Exception message: {e_message}\n"
    log_message += "---------------------------------------------------------------------------------------------\n"
    log_message += "---------------------------------------------------------------------------------------------"

    if log_file:
        logging.basicConfig(filename=log_file, level=level)
    else:
        logging.basicConfig(level=level)

    logger.log(level, log_message)


#######################################
# Config load function
#######################################

def cfg_load(path):
    try:
        return json.load(open("configs/"+str(path)+".json"))
    except FileNotFoundError as e:
        exceptions(e)
    except Exception as e:
        exceptions(e)    




#######################################
# Database releated functions
#######################################

