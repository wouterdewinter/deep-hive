import os

"""Defines user configurable settings for application
"""
class Config:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    IMAGE_SIZE = 128
    IMAGE_PATH = 'data/catsdogs'
