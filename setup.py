from setuptools import setup, find_packages

setup(
    name="resource_monitor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'psutil',
        'scapy'
    ],
    entry_points={
        'console_scripts': [
            'start-monitor=scripts.start_monitor:main',
        ]
    },
)
