from registry import Plugins
from writers import PlistWriter, Writers


def main():
    plugins = Plugins.get()
    dayone_entries = []
    for plugin in plugins:
        try:
            dayone_entries.extend(plugin.run())
            to_write = Writers.from_entries(map(PlistWriter, dayone_entries))
            # to_write.write("/Users/rjames/Library/Group Containers/5U8NS4GX82.dayoneapp2/Data/Auto Import/Default Journal.dayone")
            to_write.write("/Users/rjames/Dropbox/Apps/Day One/Journal.dayone")
        except Exception:
            continue
        else:
            plugin.on_success()

if __name__ == '__main__':
    main()
