import logging, os

basePath = os.getcwd()
log = logging
log.basicConfig(
    filename=f'{basePath}/app.log',
    level=logging.INFO,
    format='%(asctime)s * %(levelname)s * %(message)s'
    )