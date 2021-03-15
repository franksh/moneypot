import setuptools
from setuptools import setup
from pathlib import Path
import os
import sys


from setuptools.command.develop import develop

# get __version__, __author__, and __email__
exec(open(Path(".")/"moneypot"/"metadata.py").read())
        
with open('requirements.txt','r') as f:
    install_requires = [ s.replace('\n','') for s in f.readlines() ]

class CustomDelevopInstall(develop):
    """
    Add some additional steps to setup
    (configure service, create configs, ...)
    """
    def run(self):

        develop.run(self)

        from moneypot.paths import get_package_configs, get_package_root
        from moneypot.utils import create_configs, create_logs_directory

        create_configs()
        create_logs_directory()

        # Configure supervisor
        def configure_supervisor():
            os.system("echo 'configuring supervisor'")
            path_supervisor_cfg = get_package_configs() / 'supervisor.cfg'
            # Export path to scripts so it can be used in supervisor cfg
            path_scripts = get_package_root() / 'scripts'
            os.environ['PATH_MONEYPOT_SCRIPTS'] = str(path_scripts)
            os.system(f"supervisord -c {path_supervisor_cfg}")
            os.system(f"supervisorctl reread") # reread the config file if already running
            os.system(f"supervisorctl update")

        configure_supervisor()



setup(name='moneypot',
      cmdclass={
          'develop': CustomDelevopInstall
      },
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
          entry_points = {
            'console_scripts': [
                    'moneypot = moneypot.cli:main',
                ],
        },
      zip_safe=False,
  )
