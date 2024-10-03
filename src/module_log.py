import logging


logging.basicConfig(format="[%(asctime)s][%(levelname)-8s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
