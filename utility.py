"""
Utility functions Linguistic Evidence
"""
import logging


class DisableLogger():
    """ disable logging
    """
    def __enter__(self):
       logging.disable(logging.CRITICAL)
    def __exit__(self, a, b, c):
       logging.disable(logging.NOTSET)
