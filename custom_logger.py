import logging
import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and file handler set level to debug
ch = logging.StreamHandler()
fh = logging.FileHandler('logger.log')
rh = logging.handlers.RotatingFileHandler('r_logger.log', maxBytes=1000*1000*200, backupCount=2)
logger.addHandler(rh)

ch.setLevel(logging.DEBUG)
fh.setLevel(logging.DEBUG)
rh.setLevel(logging.DEBUG)

# create formatter
StreamHandlerformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
FileHandlerformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
RotatingFileHandlerformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(threadName)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to ch
ch.setFormatter(StreamHandlerformatter)

# add formatter to fh
fh.setFormatter(FileHandlerformatter)

rh.setFormatter(RotatingFileHandlerformatter)


logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(rh)