"""
Module with utilities for development/testing
"""


from types import ModuleType as _ModuleType


class _mockall:
    def __call__(cls, *args, **kwargs):
        return None
        
    def __get__(cls, *args, **kwargs):
        return None

_mockall = _mockall()


class _ModuleStandIn(_ModuleType):
    """Mock module to use as a "standin in" for missing dependencies.

    Dotted lookup on attributes of this module will never fail but properties 
    will be None and callables will return None. Should only be used for
    development of features that do not require the missing module to exist.
    """
    def __getattr__(cls, *args, **kwargs):
        return _mockall


gpiostandin = _ModuleStandIn('gpio')
