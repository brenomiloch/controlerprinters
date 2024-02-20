from setuptools import setup

setup(
    name='MyApp',
    version='1.0',
    description='My Kivy app',
    author='Your Name',
    author_email='your.email@example.com',
    packages=['kivy'],
    install_requires=[
        'kivy',
    ],
    entry_point={
        'console_scripts': [
            'myapp=main:run',
        ],
    },
)
