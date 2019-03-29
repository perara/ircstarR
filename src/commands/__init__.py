import inspect
from os.path import dirname
import glob
import importlib.util

modules = [f for f in glob.glob(dirname(__file__)+"/*.py") if not f.endswith('__init__.py')]

__commands__ = {}

for module in modules:

    spec = importlib.util.spec_from_file_location("arbitrary.module", module)
    fns = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fns)

    functions_list = [o for o in inspect.getmembers(fns) if hasattr(o[1], "__decorated__")]

    for fn_name, fn in functions_list:
        spec = inspect.getfullargspec(fn)

        print(f"Loaded command '{fn_name.lower()}'")
        __commands__[fn_name.lower()] = fn() if inspect.isclass(fn) else fn


def load():
    return __commands__
