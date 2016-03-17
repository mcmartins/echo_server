import datetime
import logging

__log_file = 'Server-{0}.log'.format(datetime.datetime.now().strftime("%Y%m%d"))


# just to make sure the logging module is initialized and is coherent from now on
def initialize(verbose=False):
    __handler = logging.FileHandler(__log_file)
    __formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    __handler.setFormatter(__formatter)
    logging.getLogger().addHandler(__handler)
    if verbose:
        logging.getLogger().setLevel('DEBUG')
    else:
        logging.getLogger().setLevel('INFO')
