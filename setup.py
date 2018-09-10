from setuptools import setup

with open('README.rst') as fp:
    readme = fp.read()

setup(
    name='abadge',
    description='Generate badges/shields with pure HTML/CSS.',
    long_description=readme,
    version='0.2.1',
    url='https://github.com/Gustra/abadge',
    author='Gunnar Strand',
    author_email='Gurra.Strand@gmail.com',
    py_modules=['abadge'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=[],
    data_files=[],
    options={},
)
