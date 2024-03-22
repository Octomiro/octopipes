import pathlib
from setuptools import find_packages
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='octopipes',
    version='0.2.3',
    description='Pipeline library for AI workflows.',
    author='Octomiro',
    author_email='contact@octomiro.ai',
    url='https://github.com/octomiro/octopipes',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        'pydantic',
        'multiprocess',
        'numpy',
        'tqdm',
        'cmap'
    ],
    extras_require={
        'opencv': ['opencv-python'],
        'pytorch': ['torch', 'torchvision']
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License'
    ]
)
