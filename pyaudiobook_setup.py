
import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Rahul Kumar",
    author_email="kum28ra@gmail.com",
    name='pyaudiobook',
    license="MIT",
    description='pyaudiobook is a python package which converts pdf to mp3 files',
    version='v0.0.5',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Rahul-157/AudioBook',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['gtts','pdfminer'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education',
        'Topic :: Multimedia :: Sound/Audio',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
    ],
)