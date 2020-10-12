"""
    Run the program.
    Author: Radosław Piwowarski
"""
import mainLib
import os
import logging
from datetime import datetime

logger_name = "log"
debug = True


def clear_log_file(filename):
    with open(filename, "w") as f:
        pass


def main():
    clear_log_file(logger_name)
    logging.basicConfig(filename=logger_name)
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)

    logging.debug("Program starts at {0}".format(datetime.now().strftime("%d/%m/%Y, %H:%M")))
    mainLib.main()


if __name__ == '__main__':
    main()
