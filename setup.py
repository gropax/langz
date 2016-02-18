from setuptools import setup

setup(name='langz',
      version='0.0.0',
      description='Tools for manipulating multiple languages',
      url='http://www.github.com/gropax/langz',
      author='gropax',
      author_email='maximedelaudrin@gmail.com',
      license='MIT',
      packages=['langz'],
      scripts=['bin/cmn', 'bin/cmn-yellow'],
      zip_safe=False)
