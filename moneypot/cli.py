"""
Provides a CLI to the moneypot.scripts module.
"""

import sys, os
from optparse import OptionParser
import importlib
import simplejson as json
from textwrap import TextWrapper

from moneypot.paths import get_package_scripts 

def _err(msg=1):
    sys.exit(msg)

def _get_module(name):
    """
    Load the specified script from ``moneypot.scripts``
    """
    
    try:
        mod = importlib.import_module("moneypot.scripts." + name)
    except ModuleNotFoundError as e:
        if name in str(e):
            _err("Command '" + name + "' unknown.")
        else:
            raise

    return mod

# custom optparser to allow linebreaks in epilog
class _EpilogParser(OptionParser):
    def format_epilog(self, formatter):
        return self.expand_prog_name(self.epilog)

def main():
    """
    This function loads all scripts from ``moneypot.scripts``
    and provides a CLI to each of them.
    """

    description = """
  Commands:
  =========
  """

    scripts = get_package_scripts()

    wrapper = TextWrapper(subsequent_indent='    ')
    modules = {}
    for s in scripts:

        module = _get_module(s)
        modules[s] = module

        this_command = s + "  "
        this_command += str(module.__doc__)

        description += "\n  " + '\n'.join(wrapper.wrap(this_command)) + "\n"

    usage = "Usage: %prog [options] COMMAND"
    parser = _EpilogParser(usage=usage, epilog=description)
    parser.add_option("-k","--kwargs", dest="kwargs",
                      help="Keyword arguments (in form of json) that will be forwarded to the command function")
    
    (options, args) = parser.parse_args()

    if len(args) == 0:
        _err("Please specify a command.")

    if options.kwargs is not None:
        kwargs = json.loads(options.kwargs)
    else:
        kwargs = {}

    if args[0]=='supervisor':
        if len(args)>1:
            os.system(f"supervisorctl " + " ".join(args[1:]))
        else:
            _err("Please provide command to supervisor.")
    else:
        for scriptname in args:            
            if scriptname in modules:            
                modules[scriptname].main(**kwargs)
            else:
                _err("Command '" + scriptname + "' unknown.")

def run_script(name,**kwargs):
    """
    Load a script and run its main function.
    Parameters
    ==========
    name : str
        Name of the script.
    **kwargs : dict
        Additional keyword arguments to be passed to the script.
    """

    # obtain the correct script module
    mod = _get_module(name)
    # run the script's main function
    mod.main(**kwargs)


if __name__=="__main__":
    main()