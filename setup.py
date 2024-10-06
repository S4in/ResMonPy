from setuptools import setup, find_packages

setup(
    name="ResMonPy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'psutil',
        'scapy'

    ],
    entry_points={
        'console_scripts': [
            'resmon=resmonpy.main:main',
        ]
    },
)
