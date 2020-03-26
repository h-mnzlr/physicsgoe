import unittest
from pkgutil import walk_packages
from pathlib import Path
from importlib import import_module



class TestPackage(unittest.TestCase):

    def test_imports(self):
        top_package = __name__.split('.')[0]
        for module in walk_packages([top_package], f'{top_package}.'):
            if not module.ispkg:
                try:
                    imported = import_module(module.name)
                except ImportError as err:
                    self.fail(f'Importing modules failed with message:\n\t{err}')
