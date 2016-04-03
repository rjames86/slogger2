from tqdm import tqdm

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

TEMPLATE = u"""\
# Instagram Photo

{0.caption}

## Likes ({0.media.like_count})

{0.likes}

{0.comments}

"""


class InstagramPhoto(object):
    def __init__(self, media, client):
        self.media = media
        self.client = client

    def __repr__(self):
        return "<InstagramPhoto(%r)>" % self.media.id

    @property
    def caption(self):
        return self.media.caption.text if self.media.caption else ''

    @property
    def entry_text(self):
        return TEMPLATE.format(self)

    @property
    def image(self):
        return Image(self.media.get_standard_resolution_url())

    @property
    def tags(self):
        return [t.name for t in self.media.tags]

    @property
    def location(self):
        if hasattr(self.media, 'location'):
            return Location(place_name=self.media.location.name,
                            **self.media.location.point.__dict__)
        return None

    @property
    def comments(self):
        if not self.media.comments:
            return ''
        else:
            to_ret = "## Comments\n\n"
        for comment in self.media.comments:
            to_ret += u"> {}: {} - {}\n".format(str(comment.created_at),
                                                comment.text,
                                                comment.user.full_name or comment.user.username)
        return to_ret

    @property
    def likes(self):
        to_ret = ""
        for person in [user.full_name or user.username
                       for user in self.client.media_likes(self.media.id)]:
            to_ret += u"- {0}\n".format(person)
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

    def __init__(self, context):
        self.context = context
        self._client = None
        self._recent_media = []

    @property
    def client(self):
        if not self._client:
            self._client = InstagramAPI(access_token=self.AUTH_TOKEN, client_secret=self.SECRET)
        return self._client

    def run(self):
        instagram_photos = [InstagramPhoto(i, self.client) for i in self.recent_media()]
        to_ret = []
        for ip in tqdm(instagram_photos):
            to_ret.append(DayOneEntry.from_object(ip))
        return to_ret

    def cache_data(self):
        to_ret = {}
        if self.recent_media():
            to_ret['min_id'] = self.recent_media()[0].id
        elif 'min_id' in self.context['cache']:
            return self.context['cache']
        return to_ret

    def recent_media(self):
        if not self._recent_media:
            cache = self.context.get('cache', {})
            rm, next_ = self.client.user_recent_media(**cache)
            self._recent_media.extend(rm)
            while next_:
                print "getting recent media next..."
                rm, next_ = self.client.user_recent_media(with_next_url=next_, **cache)
                self._recent_media.extend(rm)
            self._recent_media[:] = [m for m in self._recent_media
                                     if m.id != cache.get('min_id') and
                                     m.type == 'image']
        return self._recent_media
