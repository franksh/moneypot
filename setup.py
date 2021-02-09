from setuptools import setup
from pathlib import Path
import os
import sys

# get __version__, __author__, and __email__
exec(open(Path(".")/"moneypot"/"metadata.py").read())

with open('requirements.txt','r') as f:
    install_requires = [ s.replace('\n','') for s in f.readlines() ]

setup(name='moneypot',
      version=__version__,
      license=__license__,
      author=__author__,
      author_email=__email__,
      description='making money on the stonkmarket',
      long_description='',
      url='https://github.com/franksh/moneypot',
      packages=setuptools.find_packages(),
      install_requires=install_requires,
      python_requires='>=3.7',
      dependency_links=[
      ],
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      tests_require=['pytest', 'pytest-cov'],
      project_urls={
          'Documentation': 'TODO',
          'Contributing Statement': 'https://github.com/franksh/moneypot/blob/master/CONTRIBUTING.md',
          'Bug Reports': 'https://github.com/franksh/moneypot/issues',
          'Source': 'https://github.com/franksh/moneypot/',
      },
      include_package_data=True,
      zip_safe=False,
  )
