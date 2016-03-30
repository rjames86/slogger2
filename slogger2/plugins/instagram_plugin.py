from instagram.client import InstagramAPI

from dayone_entry import (
    DayOneEntry,
    Image,
    Location,
)
from registry import Plugin
from config import (
    INSTAGRAM_TOKEN,
    INSTAGRAM_SECRET
)

TEMPLATE = """\
# Instagram Photo

{0.caption}

## Likes ({0.like_count})

{0.likes}

"""


class InstagramPhoto(object):
    def __init__(self, media, client):
        self.media = media
        self.client = client

    def __getattr__(self, name):
        if hasattr(self.media, name):
            return getattr(self.media, name)
        else:
            # Default behaviour
            raise AttributeError

    def __repr__(self):
        return "<InstagramPhoto(%r)>" % self.media.id

    @property
    def caption(self):
        return self.media.caption.text.encode('utf-8')

    @property
    def entry_text(self):
        return TEMPLATE.format(self)

    @property
    def image(self):
        return Image(self.media.images['standard_resolution'])

    @property
    def location(self):
        if hasattr(self.media, 'location'):
            return Location(place_name=self.media.location.name, **self.media.location.point.__dict__)
        return None

    @property
    def likes(self):
        to_ret = ""
        for person in [user.full_name or user.username for user in self.client.media_likes(self.media.id)]:
            to_ret += "- {0}\n".format(person.encode("utf-8")).decode('utf-8')
        return to_ret

    @property
    def starred(self):
        return False

    @property
    def created(self):
        return self.media.created_time


class Instagram(Plugin):
    AUTH_TOKEN = INSTAGRAM_TOKEN
    SECRET = INSTAGRAM_SECRET

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = InstagramAPI(access_token=self.AUTH_TOKEN, client_secret=self.SECRET)
        return self._client

    def run(self):
        instagram_photos = [InstagramPhoto(i, self.client) for i in self.recent_media()]
        return map(DayOneEntry.from_object, instagram_photos)

    def recent_media(self):
        to_ret = []
        rm, next_ = self.client.user_recent_media()
        to_ret.extend(rm)
        while next_:
            rm, next_ = self.client.user_recent_media(with_next_url=next_)
            to_ret.extend(rm)
        return to_ret
