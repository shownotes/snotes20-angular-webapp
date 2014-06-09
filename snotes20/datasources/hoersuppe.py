from .AbstractDataSource import AbstractDataSource
from datetime import datetime
import hoerapi
import snotes20.models.podcast as models


class HoersuppeDataSource(AbstractDataSource):
    name = 'hoersuppe'
    shortname = models.SOURCE_HOERSUPPE

    @classmethod
    def get_podcasts(cls):
        h_podcastlist = hoerapi.get_podcasts()
        podcasts = []

        for pod in h_podcastlist:
            data = hoerapi.get_podcast_data(pod.slug)

            type = None

            if data.rundfunk:
                type = models.TYPE_RADIO
            else:
                type = models.TYPE_PODCAST

            podcasts.append(models.Podcast(
                slug=data.slug,
                creator=None,
                title=data.title,
                description=data.description,
                url=data.url,
                stream=None,
                chat=data.chat_url,
                type=type,
                create_date=datetime.now(),
                source=cls.shortname,
                source_id=data.id
            ))

        return podcasts

    @classmethod
    def get_episodes(cls, date_start, date_end):
        h_episodes = hoerapi.get_live(dateStart=date_start, dateEnd=date_end)
        episodes = []

        for ep in h_episodes:
            podcast = models.Podcast.objects.get(slug=ep.podcast)

            episodes.append(models.Episode(
                podcast=podcast,
                creator=None,
                number=None,
                episodeurl=None,
                date=ep.livedate,
                canceled=False,
                type=podcast.type,
                create_date=datetime.now(),
                stream=ep.streamurl,
                source=cls.shortname,
                source_id=ep.id,
            ))

        return episodes
