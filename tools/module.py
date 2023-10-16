import aiomysql
import asyncio
import time
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
    log_message += f"Exception args: {e.args}\n" 

    if hasattr(e, 'cause'):
        log_message += f"Cause: {e.cause}\n"  

    log_message += "---------------------------------------------------------------------------------------------\n"
    log_message += "---------------------------------------------------------------------------------------------"

    if log_file:
        logging.basicConfig(filename=log_file, level=level)
    else:
        logging.basicConfig(level=level)

    logger.log(level, log_message)
    time.sleep(0.3)

#######################################
# Config load function
#######################################


def cfg_load(file_name, dir = "configs/"):
    try:
        return json.load(open(dir+str(file_name)+".json"))
    except FileNotFoundError as e:
        exceptions(e)
    except Exception as e:
        exceptions(e)    

cfg = cfg = cfg_load("config")

#######################################
# Database releated functions
#######################################


#database connection function
async def set_db_conn():
    try:
        conn = await aiomysql.create_pool(
            host = cfg["database"]["host"],
            port = cfg["database"]["port"],
            user = cfg["database"]["user"],
            password = cfg["database"]["password"],
            db = cfg["database"]["db"],
            minsize = cfg["database"]["minsize"],
            maxsize = cfg["database"]["maxsize"]
        )
        return conn
    except Exception as e:
        exceptions(e)
        return None


#function that start database connection
async def get_db_conn(pool):
    try:
        conn = await pool.acquire()
        return conn
    except Exception as e:
        exceptions(e)
        return None
    

#fuction that release current database connection
async def release_db_conn(cursor, db_conn, pool):
    try:
        if cursor:
            await cursor.close()
        if db_conn:
            await pool.release(db_conn)
    except Exception as e:
        exceptions(e)        



#function that will terminate database connection
async def close_db_conn(pool):
    try:
        pool.close()
        await pool.wait_closed()        
    except Exception as e:
        exceptions(e)        


#function that will return you data from the database
async def db_get_data(sql, cursor, mode=None, *args, **kwargs):
    try:
        all_args = args + tuple(kwargs.values())
        await cursor.execute(sql, all_args)
        if mode == 1:
            data = await cursor.fetchone()
        else:
            data = await cursor.fetchall()
        return data
    except Exception as e:
        exceptions(e)


#function that will manipulate with the database data
async def db_manipulate_data(sql, cursor, db_conn, commit, *args, **kwargs):
    try:
        all_args = args + tuple(kwargs.values())
        await cursor.execute(sql, all_args)
        if commit:
            await db_conn.commit()
    except Exception as e:
        exceptions(e)
        