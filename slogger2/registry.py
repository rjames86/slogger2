import pkgutil
import imp
import os


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        if not hasattr(cls, 'plugins'):
            # Called when the metaclass is first instantiated
            cls.plugins = []
        else:
            # Called when a plugin class is imported
            cls.register_plugin(cls)

    def register_plugin(cls, plugin):
        """Add the plugin to the plugin list and perform any registration logic"""

        # create a plugin instance and store it
        # optionally you could just store the plugin class and lazily instantiate
        instance = plugin()
        print "registering plugin", instance

        # save the plugin reference
        cls.plugins.append(instance)


class Plugin(object):
    __metaclass__ = PluginMount

    DISABLED = False

    tags = None
    starred = False
    location = None

    def load(self, *paths):
        paths = list(paths)
        for _, name, _ in pkgutil.iter_modules(paths):
            fid, pathname, desc = imp.find_module(name, paths)
            try:
                print name, fid, pathname, desc
                imp.load_module(name, fid, pathname, desc)
            except Exception as e:
                print "could not load plugin module '%s': %s" % (pathname, e.message)
            if fid:
                fid.close()

    def run(self):
        """
        Should return a list of objects which should map to a DayOneEntry object

        ::entry_text (required)
        ::created (optional)
        ::tags (optional)
        ::starred (optional)
        ::location (optional)
        """
        raise NotImplemented("You must implement `run` from within your plugin")


class Plugins(list):
    @classmethod
    def get(cls):
        self = cls()
        plugin_class = Plugin()
        plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
        plugin_class.load(plugin_path)
        self.extend(plugin_class.plugins)
        return self
