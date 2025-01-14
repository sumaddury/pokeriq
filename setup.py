from setuptools import setup, find_packages

# setup.py

setup(
    name='pokeriq', 
    version='0.1.0',      
    packages=find_packages(),  
    install_requires=[
        'scipy>=1.2.0'
    ],     
    description='A Micro-Library for Holdem Simulation',  
    python_requires='>=3.7',  
    url='https://github.com/sumaddury/pokeriq',
    author='Sucheer Maddury',
    author_email='sm2939@cornell.edu'
)
