from registry import Plugins
from writers import PlistWriter, Writers

def main():
    plugins = Plugins.get()
    dayone_entries = []
    print "getting dayone entries"
    for plugin in plugins:
        try:
            dayone_entries.extend(plugin.run())
            print "creating writers"
            to_write = Writers.from_entries(map(PlistWriter, dayone_entries))
            print "writing..."
            # to_write.write("/Users/rjames/Library/Group Containers/5U8NS4GX82.dayoneapp2/Data/Auto Import/Default Journal.dayone")
        except:
            print "failed. skipping"
            continue
        else:
            plugin.on_success()



if __name__ == '__main__':
    main()
