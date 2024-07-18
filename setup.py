from setuptools import setup, find_packages

setup(
    name='GDUtilities',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'python-dotenv',
    ],
    author='0x7C2f',
    author_email='0x7C2f@grimdevelopment.com',
    description='A collection of utility functions for data processing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GrimDevelopment/GDUtilities',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
