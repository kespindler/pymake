from setuptools import setup

setup(name='pymake2',
    version='0.1',
    description='Python make',
    url='http://github.com/kespindler/pymake',
    author='Kurt Spindler',
    author_email='kespindler@gmail.com',
    license='MIT',
    packages=['pymake'],
    entry_points={
      'console_scripts': [
          'pymake = pymake:main',
          ]
      }
)
