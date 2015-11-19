import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


import newtwitter
MODULES = {
    'newModule' : [
            newModule.NewModuleParser(),
            newModule.create_output_manager(False),
        ],
    }
