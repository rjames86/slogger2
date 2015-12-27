from instagram.client import InstagramAPI

from registry import Plugin
from config import (
    INSTAGRAM_TOKEN,
    INSTAGRAM_SECRET
)

TEMPLATE = """\
# Instagram Photo

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
        return TEMPLATE.format(self)

    @property
    def likes(self):
        to_ret = ""
        for person in [user.full_name or user.username for user in self.client.media_likes(self.media.id)]:
            to_ret+= "- {0}\n".format(person)
        return to_ret


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
        to_ret = []
        for i in self.recent_media():
            to_ret.append(InstagramPhoto(i, self.client))
        return to_ret

    def recent_media(self):
        to_ret = []
        print "getting"
        rm, next_ = self.client.user_recent_media()
        to_ret.extend(rm)
        while next_:
            print "getting next"
            rm, next_ = self.client.user_recent_media(with_next_url=next_)
            to_ret.extend(rm)
        return to_ret
