import distutils.core
from distutils.core import setup

version_number = '0.1'
setup(name = 'qvalue',
      version = version_number,
      description = 'Converts p-values in q-values in order to account for multiple hypotheses testing, see (Storey and Tibshirani, 2003)',
      long_description = open('README.txt').read(),
      author = 'Nicolo Fusi',
      author_email = 'nicolo.fusi@sheffield.ac.uk',
      install_requires = ['numpy >= 1.5',
                          'scipy >= 0.8',
                          'numba >= 0.2'],
      license = '3-clause BSD',
      )
