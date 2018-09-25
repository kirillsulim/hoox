from setuptools import setup, find_packages
from os import path


project_directory = path.abspath(path.dirname(__file__))

data_files = []

def load_from(file_name):
    data_files.append(file_name)
    with open(path.join(project_directory, file_name), encoding='utf-8') as f:
        return f.read()

setup(
    name='hoox',
    version=load_from('hoox.version').strip(),
    url='https://github.com/kirillsulim/hoox',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    description='Git hooks manager',
    long_description=load_from('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': '*'},
    include_package_data=True,
    data_files=[
        ('.', data_files),
    ],
    entry_points={
        'console_scripts': [
            'hoox = hoox.hoox:main',
        ]
    },
    install_requires=[
    ],
    classifiers=(
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
