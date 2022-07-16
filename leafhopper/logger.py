import logging

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.INFO
    )
setup_logging()

logger = logging.getLogger('leafhopper')