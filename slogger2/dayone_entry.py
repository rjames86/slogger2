import md5
import uuid
import requests
import os


class Location(object):
    def __init__(self, administrative_area=None, latitude=None, longitude=None, place_name=None):
        self.administrative_area = administrative_area
        self.latitude = latitude
        self.longitude = longitude
        self.place_name = place_name

    def to_dict(self):
        return {
            'Administrative Area': '',
            'Country': '',
            'Latitude': self.latitude,
            'Longitude': self.longitude,
            'Place Name': self.place_name
        }


class Image(object):
    def __init__(self, image_url):
        self.url = image_url
        self._as_string = None

    @property
    def as_string(self):
        if not self._as_string:
            self._as_string = self.download_file()
        return self._as_string

    def save_to_file(self, journal_location, uuid):
        print "saving image to file"
        with open(os.path.join(journal_location, "photos", "%s.jpg" % uuid), 'wb') as f:
            f.write(self.as_string)

    def download_file(self):
        print "downloading image", self.url
        to_ret = ""
        r = requests.get(self.url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                to_ret += chunk
        return to_ret


class DayOneEntry(object):
    def __init__(self, entry_text, created=None, tags=None, location=None, starred=False, image=None):
        print "dayone entry creating"
        assert (isinstance(location, Location) or not location), "location must be an instance of Location"
        assert (isinstance(image, Image) or not image), "image must be an instance of Image"

        self.entry_text = entry_text
        self._created = created
        self.tags = tags
        self.location = location
        self.starred = starred
        self.image = image

        self._uuid = None

    @property
    def created(self):
        return self._created.isoformat()

    def __repr__(self):
        return "<DayOneEntry(%r)" % self.uuid

    @property
    def uuid(self):
        if not self._uuid:
            md5_entry_text = md5.new(self.entry_text)
            self._uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, md5_entry_text.digest())).replace('-', '')
        return self._uuid

    @classmethod
    def from_object(cls, obj):
        return cls(
            obj.entry_text,
            created=obj.created,
            tags=obj.tags,
            location=obj.location,
            starred=obj.starred,
            image=obj.image
        )
