"""
    Run the program.
    Author: Radosław Piwowarski
"""
import mainLib
import logging
from datetime import datetime
import argparse

logger_name = "log"
debug = True


def parser_func() -> argparse.ArgumentParser:
    parser_main = argparse.ArgumentParser(description="NWNTool")
    # Install
    parser_main.add_argument("-i", "--install", help="Installs NWNTool to store data on disk.", default=".")
    # Run
    parser_main.add_argument("-r", "--run", help="Runs the program interactively.", default=".")
    # List modules on disk
    parser_main.add_argument("-ls", action="store_true", help="Lists modules found on disk.")
    # List modules on vault #TODO: Add categories to filter the list!
    parser_main.add_argument("-lsv", action="store_true", help="Lists modules from https://neverwintervault.org")
    # Verbosity
    parser_main.add_argument("-v", action="count", help="Increase verbosity.", default=1)
    parser_main.add_argument("--verbosity", type=int, choices=[0, 1, 2],
                             help="Verbosity level: 0 - silent, 1 - user info, 2 - debug info", default=1)
    # Search for module
    parser_main.add_argument("-s", "--search", help="Search for module {name}.")
    # Disk usage
    parser_main.add_argument("-d", "--disk-usage", choices=["DE", "EE", ""], default="",
                             help="""Prints total amount of data stored in tracked directories.
                                     DE - Diamond Edition only,
                                     EE - Enhanced Edition only,
                                     An empty string represents both versions (default).""")
    return parser_main


def install() -> bool:
    u"""Install."""
    return False


def main(*args, **kwargs):
    logger = logging.getLogger()

    parser = parser_func()
    args = parser.parse_args()
    print(vars(args))

    if debug:
        logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logger_name, mode="w")
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

    # module = nwn_diamond.download_module_from_vault(kwargs["www"], "enigma")
    # nwn_diamond.create_module_from_scrapper_data(module)


if __name__ == '__main__':
    website_with_module = "https://neverwintervault.org/project/nwn1/module/enigma-island-complete"
    main(www=website_with_module)
