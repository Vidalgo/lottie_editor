from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Lottie builder package'

# Setting up
setup(
    name="lottiebuild",
    version=VERSION,
    author="Avidor Rabinovich",
    author_email="<avidor@vidalgo.ai>",
    description=DESCRIPTION,    
    packages=find_packages(),
    install_requires=['Pillow', 'numpy'],
    keywords=['python', 'lottie', 'animation', 'vector graphics'],
    classifiers=[
        "Development Status :: 1 - development",
        "Intended Audience :: Lottie Files Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
