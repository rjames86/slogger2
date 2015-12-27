import md5
import uuid
import requests

class Location(object):
    def __init__(self, administrative_area=None, latitude=None, longitude=None, place_name=None):
        self.administrative_area = administrative_area
        self.latitude = latitude
        self.longitude = longitude
        self.place_name = place_name


class Image(object):
    def __init__(self, image_url):
        self.url = image_url
        self._as_string = None

    @property
    def as_string(self):
        if not self._as_string:
            self._as_string = self.download_file()
        return self._as_string

    def download_file(self):
        to_ret = ""    
        r = requests.get(self.url, stream=True)
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                to_ret += chunk
        return to_ret


class DayOneEntry(object):
    def __init__(self, entry_text, created=None, tags=None, location=None, starred=False, image=None):
        assert (isinstance(location, Location) or not location), "location must be an instance of Location"
        assert (isinstance(image, Image) or not image), "image must be an instance of Image"


        self.entry_text = entry_text
        self.created = created
        self.tags = tags
        self.location = location
        self.starred = starred
        self.image = image

    @property
    def uuid(self):
        md5_entry_text = md5.new(self.entry_text)
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, md5_entry_text.digest())).replace('-', '')

    @classmethod
    def by_object(cls, obj):
        return cls(
            obj.entry_text,
            created=obj.created,
            tags=obj.tags,
            location=obj.location,
            starred=obj.starred
            image=obj.image
        )
