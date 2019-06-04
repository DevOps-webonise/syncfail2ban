from distutils.core import setup

setup(
    name='sync2failban',
    version='0.1dev',
    url='webonise.com',
    author='Justin Fortier',
    author_email='justin.fortier@weboniselab.com',
    packages=['peewee','pprint', 'pyyaml', 'pymysql'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)
