"""
    Run the program.
    Author: Radosław Piwowarski
"""
import mainLib
import os
import logging
from datetime import datetime

logger_name = "log"


def clear_log_file(filename):
    with open(filename, "w") as f:
        pass


def main():
    clear_log_file(logger_name)
    logging.basicConfig(filename=logger_name, level=logging.DEBUG)
    logging.debug("Program starts at {0}".format(datetime.now().strftime("%d/%m/%Y, %H:%M")))


if __name__ == '__main__':
    main()
