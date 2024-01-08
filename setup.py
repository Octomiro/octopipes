from setuptools import find_packages
from setuptools import setup


setup(
    name='octopipes',
    version='0.1.0',
    description='Pipeline library for AI workflows.',
    author='Octomiro',
    author_email='contact@octomiro.ai',
    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        'pydantic',
        'multiprocess',
        'numpy',
        'tqdm',
        'cmap'
    ],
    extras_require={
        'opencv': ['opencv-python']
    }
)
