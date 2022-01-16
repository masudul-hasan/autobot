import os
from pathlib import Path

'''
This page is all about static data that won't be changed through the Tests. 
All the time this data should be static as-is like here

written by: jiaul_islam
'''

# ALL GLOBAL VARIABLE
BASE_DIR = Path.cwd()
READER_FILENAME = 'Request_CR.xlsx'
WRITER_FILENAME = 'Output_CR.xlsx'
CANCEL_CHANGE_FILENAME = "cancel.txt"
CLOSE_CHANGE_FILENAME = "close.txt"


class StaticData:
    IT_HOME = 'IT Home'
    READ_EXCEL_FILE = str(BASE_DIR.joinpath("data_driver", READER_FILENAME))
    WRITE_EXCEL_FILE = str(BASE_DIR.joinpath("data_driver", WRITER_FILENAME))
    CANCEL_CHANGE_TXT_FILE_PATH = str(BASE_DIR.joinpath("data_driver", CANCEL_CHANGE_FILENAME))
    CLOSE_CHANGE_TXT_FILE_PATH = str(BASE_DIR.joinpath("data_driver", CLOSE_CHANGE_FILENAME))
    VIEW_ATTACHMENT_DEFAULT_STATE = 'View Attachment Disabled'


class BMCData:
    BMC_URL = 'http://itsm-web.robi.com.bd:8080/arsys/shared/login.jsp?/arsys/home'
    USERNAME = 'mas1171'  # Get the username
    PASSWORD = 'Robi@123'  # Get the password


class LDMAData:
    LDMA_URL = 'http://ldma.robi.com.bd/view/common/login.php'
    LDMA_USERNAME = os.environ.get("LDMA_USER")
    LDMA_PASSWORD = os.environ.get("LDMA_PASS")
