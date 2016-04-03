import pkgutil
import imp
import os

import shelve
import datetime


class LastRun(object):

    def _get_db(self):
        return shelve.open('lastrun')

    def __enter__(self):
        self.lastrun_db = self._get_db()
        return self

    def __exit__(self, type, value, traceback):
        self.lastrun_db.close()

    @staticmethod
    def get_last_run():
        with LastRun() as lr:
            return lr.lastrun_db.get('last_run_time') or None

    @staticmethod
    def set_last_run():
        with LastRun() as lr:
            lr.lastrun_db['last_run_time'] = datetime.datetime.now()

    @staticmethod
    def save_plugin_info(plugin, info):
        with LastRun() as lr:
            lr.lastrun_db[plugin.__class__.__name__] = info
            return

    @staticmethod
    def get_plugin_info(plugin):
        with LastRun() as lr:
            return lr.lastrun_db.get(plugin.__name__, {})


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
        last_run = LastRun.get_last_run()
        plugin_context = LastRun.get_plugin_info(plugin)
        instance = plugin(dict(last_run=last_run, cache=plugin_context))

        # save the plugin reference
        cls.plugins.append(instance)


class Plugin(object):
    __metaclass__ = PluginMount

    DISABLED = False

    tags = None
    starred = False
    location = None

    def __repr__(self):
        return "<Plugin(%r)>" % self.__class__.__name__

    def load(self, *paths):
        paths = list(paths)
        for _, name, _ in pkgutil.iter_modules(paths):
            fid, pathname, desc = imp.find_module(name, paths)
            try:
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

    def cache_data(self):
        """
        Return a dictionary of information that you'd like to store and pass to the plugin
        the next time it's run.
        """
        return None

    def on_success(self):
        if self.cache_data() is not None:
            LastRun.save_plugin_info(self, self.cache_data())
        LastRun.set_last_run()


class Plugins(list):
    @classmethod
    def get(cls):
        self = cls()
        plugin_class = Plugin()
        plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
        plugin_class.load(plugin_path)
        self.extend(plugin_class.plugins)
        return self
