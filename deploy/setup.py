from setuptools import setup

setup(
    name='Spack Deploy',
    version='0.1',
    py_modules=['spackd'],
    install_requires=[
        'Click',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        spackd=spackd:spackd
    '''
)
