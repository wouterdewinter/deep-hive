import os

class Config:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    IMAGE_SIZE = 128
    IMAGE_PATH = 'data/128x128'
