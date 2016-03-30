import datetime
import plistlib


class BaseWriter(object):
    def __init__(self, dayone_entry):
        self.dayone_entry = dayone_entry

    @property
    def items_to_dict(self):
        return {
            'Creator': {
                'Software Agent': '{0} {1}'.format('TODO', 'TODO'),
                'Generation Date': datetime.datetime.utcnow(),
            },
            'UUID': self.dayone_entry.uuid,
            'Creation Date': 'TODO',
            'Time Zone': 'TODO?',
            'Tags': self.dayone_entry.tags,
            'Starred': self.dayone_entry.starred,
            'Entry Text': self.dayone_entry.entry_text,
            'Location': {
                'Administrative Area': 'TODO',
                'Country': 'TODO',
                'Latitude': 'TODO',
                'Longitude': 'TODO',
                'Place Name': 'TODO'
            }
                }

    def generate(self):
        raise NotImplemented("You must implament `generate` within your writer class")


class PlistWriter(BaseWriter):
    def generate(self):
        return plistlib.writePlistToString(plistlib.Dict(**self.items_to_dict))
