# -*- coding: utf-8 -*-

import os, sys
from PyQt5 import QtWidgets
from src.http.http_check import first_connection_test
from src.ui.dashboard import Dashboard
import src.database.database as database

DATA_FOLDER_PATH = "data/"
CONFIG_FOLDER_PATH = "api/"

CONFIG_FILE = "api.ini"

def init_directories():
    """ 
    Initiation of the configuration and data directories, 
    creation if not present in the project. \n
    Checking the configuration files.

    TODO: Generate the configuration files if they doesn't exists.
    """

    print("Checking data directory ...")
    if not os.path.exists(DATA_FOLDER_PATH):
        try:
            print("DATA directory doesn't exist, creation ...")
            os.mkdir(DATA_FOLDER_PATH)
        except OSError:
            print("ERROR: DATA directory creation failed. \n")
        else:
            print("DATA directory successfully created.")

    print("Checking api directory ...")
    if not os.path.exists(CONFIG_FOLDER_PATH):
        try:
            print("CONFIG directory doesn't exist, creation ...")
            os.mkdir(CONFIG_FOLDER_PATH)
        except OSError:
            print("ERROR: CONFIG directory creation failed. \n")
        else:
            print("CONFIG directory successfully created.")

def run():
    init_directories()

    database.create_db()
    db = database.connect_to_db()

    if not first_connection_test():
        exit()

    application = QtWidgets.QApplication(sys.argv)
    butterscotch = Dashboard()
    butterscotch.show()
    sys.exit(application.exec_())
    

if __name__ == '__main__':
    run()