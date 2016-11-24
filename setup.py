from setuptools import setup, find_packages


setup(
    name='linux_translator',
    version="0.1",
    packages=find_packages(),
    entry_points={
       'console_scripts': [
           'linux_translator = linux_translator.app:main',
       ]
    }
)
