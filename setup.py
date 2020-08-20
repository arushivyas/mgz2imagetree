import sys

# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'mgz2imagetree',
      version          =   '1.0.0',
      description      =   '(Python) utility to filter mgz volumes to per-voxel-value directories of jpg/png image slices',
      long_description =   readme(),
      author           =   'FNNDSC',
      author_email     =   'dev@babymri.org',
      url              =   'https://github.com/FNNDSC/mgz2imagetree',
      packages         =   ['mgz2imagetree'],
      install_requires =   ['pfmisc', 'nibabel', 'numpy', 'imageio', 'pftree'],
      #test_suite       =   'nose.collector',
      #tests_require    =   ['nose'],
      scripts          =   ['bin/mgz2imagetree'],
      license          =   'MIT',
      zip_safe         =   False
)