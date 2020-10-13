"""
    Run the program.
    Author: Radosław Piwowarski
"""
import mainLib
import logging
from datetime import datetime

logger_name = "log"
debug = True


def clear_log_file(filename):
    with open(filename, "w") as f:
        pass


def main():
    clear_log_file(logger_name)
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logger_name)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    console_formatter = logging.Formatter('%(name)12s - %(levelname)8s - %(message)s')
    ch.setFormatter(console_formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.debug("Program starts at {0}".format(datetime.now().strftime("%d/%m/%Y, %H:%M")))
    mainLib.main()

    nwn = mainLib.NWN.get_instance()
    for m in nwn.show_modules():
        #print(m)
        pass

    nwn_ee = mainLib.NWN.get_instance(1)
    print(nwn_ee.path)
    for m in nwn_ee.show_modules():
        print(m)


if __name__ == '__main__':
    main()
