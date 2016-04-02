import plistlib
import os


class BaseWriter(object):
    def __init__(self, dayone_entry):
        self.dayone_entry = dayone_entry

    def items_to_dict(self):
        to_ret = {
            'UUID': self.dayone_entry.uuid,
            'Creation Date': self.dayone_entry.created,
            'Tags': self.dayone_entry.tags,
            'Starred': self.dayone_entry.starred,
            'Entry Text': self.dayone_entry.entry_text,
        }
        if self.dayone_entry.location:
            to_ret['Location'] = self.dayone_entry.location.to_dict()
        return to_ret

    def generate(self):
        raise NotImplemented("You must implament `generate` within your writer class")

    def save_images(self, journal_location):
        if self.dayone_entry.image:
            self.dayone_entry.image.save_to_file(journal_location, self.dayone_entry.uuid)

    def write(self, journal_location):
        print "writing entry", self.dayone_entry.uuid
        with open(os.path.join(journal_location, "entries", "%s.doentry" % self.dayone_entry.uuid), 'w') as f:
            f.write(self.generate())
        ## the dayone object should just be stored in the image class
        self.save_images(journal_location)


class PlistWriter(BaseWriter):
    def generate(self):
        return plistlib.writePlistToString(plistlib.Dict(**self.items_to_dict()))


class Writers(list):
    @classmethod
    def from_entries(cls, entries):
        self = cls()
        self.extend(entries)
        return self

    def write(self, journal_location):
        for entry in self:
            entry.write(journal_location)
