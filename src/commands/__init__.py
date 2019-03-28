'''
Expose every class/function from every file in commands package so we don't
have to import again when a new file with a new class/function i made

src https://stackoverflow.com/a/1057534
'''

from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

