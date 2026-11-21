#we are making the log folders so we will know where the system is crashing or it helps to debug 
import logging
import os 
from datetime import datetime

#By using this we will generate the log filename
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#Using this we will create the log folder name 

LOG_DIR =os.path.join(os.getcwd(),"logs")

#using this we will actually make the dir

os.makedirs(LOG_DIR,exist_ok=True)

#Complete log file path
LOG_FILE_PATH =os.path.join(LOG_DIR,LOG_FILE)

#This will actually creat the logfile properly insde the logs folder 
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


"""
LEVEL
DEBUG → Ignore


INFO → Save


WARNING → Save


ERROR → Save


CRITICAL → Save
"""
