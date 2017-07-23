from setuptools import setup

setup(
    name='server',
    version='0.0.1',
    install_requires = [
        'tornado',
    ],
    entry_points={
        'console_scripts' : [
            'server = server:main',
        ]
    }
)
