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
    with open(filename, "w"):
        pass


def main(*args, **kwargs):
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

    nwn_diamond, nwn_ee = mainLib.main()

    module = nwn_diamond.download_module_from_vault(kwargs["www"], "enigma")
    nwn_diamond.create_module_from_scrapper_data(module)

    l = nwn_diamond.show_modules()
    for m in l:
        print(m)


if __name__ == '__main__':
    website_with_module = "https://neverwintervault.org/project/nwn1/module/enigma-island-complete"
    main(www=website_with_module)
