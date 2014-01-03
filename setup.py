from setuptools import setup

setup(name='pymake',
      version='0.1',
      description='Python make',
      url='http://github.com/kespindler/pymake',
      author='Python Make',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['pymake'],
      entry_points={
          'console_scripts': [
              'pk = pymake:main',
              ]
          }
      )
