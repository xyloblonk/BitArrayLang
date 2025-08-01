from setuptools import setup, find_packages

setup(
    name='bitarraylang',
    version='0.1.0',
    description='Structured bitfield assembly language with VM',
    author='XyloBlonk',
    packages=find_packages(),
    install_requires=[
        'lark-parser',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
