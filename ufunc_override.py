"""
Usage:

import ufunc_override as np

define a class with __array_priority__ and __ufunc_override__.
__ufunc_override__ should be a dict keyed with ufunc names, and valued
with the callable functions you want to override them.
"""

import numpy as np

class make_overridable(object):
    def __init__(self, name):
        self.name = name
        self.__name__ = self.name.__name__
    def __call__(self, *args, **kwargs):
        # Get a list of the args that want to override.
        override_args = []
        for arg in args:
            if (hasattr(arg, '__ufunc_override__') and
                hasattr(arg, '__array_priority__')):
                    if arg.__ufunc_override__.get(self.name.__name__):
                        override_args.append(arg)
        # Sort by __array_priority__
        override_args = sorted(override_args, 
                               key=lambda arg: arg.__array_priority__)
        if override_args:
            dominant_arg = override_args[-1]
            remaining_args = [ arg for arg in args if arg is not dominant_arg]
            new_func = dominant_arg.__ufunc_override__.get(self.name.__name__)
            return new_func(dominant_arg, *remaining_args, **kwargs)
        else:
            return self.name(*args, **kwargs)


def override_all():
    for name, call in np.__dict__.items():
        if isinstance(getattr(np, name), np.ufunc):
            setattr(np, name, make_overridable(call))

def override_set_numeric_ops():
    def_ops = np.set_numeric_ops()
    new_ops ={}
    for name, call in def_ops.items():
        new_ops[name] = make_overridable(call)
    np.set_numeric_ops(**new_ops)

def np_to_global():
    for name in np.__all__:
        if name not in globals():
            globals()[name] = getattr(np, name)

override_all()
override_set_numeric_ops()
np_to_global()
