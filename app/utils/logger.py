import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('/opt/dcims/logs'):
        os.makedirs('/opt/dcims/logs')

    # Set up rotating file handler
    handler = RotatingFileHandler(
        '/opt/dcims/logs/dcims.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )

    # Set log format
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    # Set logging level
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('DCIMS startup')