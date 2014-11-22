from datetime import datetime
import logging

import hoerapi

from .AbstractDataSource import AbstractDataSource
import snotes20.models.podcast as models

logger = logging.getLogger(__name__)


class HoersuppeDataSource(AbstractDataSource):
    name = 'hoersuppe'
    shortname = models.SOURCE_HOERSUPPE

    @classmethod
    def get_podcasts(cls):
        h_podcastlist = hoerapi.get_podcasts()

        for pod in h_podcastlist:
            data = hoerapi.get_podcast_data(pod.slug)

            if data.rundfunk:
                type = models.TYPE_RADIO
            else:
                type = models.TYPE_PODCAST

            cover = models.Cover.from_url(None, data.imageurl)

            if cover is None:
                logger.debug("could not get cover for %s", pod.slug)

            yield ((
                models.Podcast(
                    creator=None,
                    title=data.title,
                    description=data.description,
                    url=data.url,
                    cover=cover,
                    stream=None,
                    chat=data.chat_url,
                    type=type,
                    import_date=datetime.now(),
                    source=cls.shortname,
                    source_id=data.id
                ),
                models.PodcastSlug(
                    slug=data.slug,
                ),
            ))

    @classmethod
    def get_episodes(cls, date_start, date_end):
        h_episodes = hoerapi.get_live(count=20, dateStart=date_start, dateEnd=date_end)
        episodes = []

        for ep in h_episodes:
            if len(ep.podcast) == 0:
                logger.warn("skipped episode %s (%s), no podcast given", ep.id, ep.title)
                continue

            try:
                podcast = models.Podcast.objects.get(slugs__slug=ep.podcast)
            except models.Podcast.DoesNotExist:
                logger.warn("can't import episode %s: podcast '%s' not found!", ep.id, ep.podcast)
                continue

            episodes.append(models.Episode(
                podcast=podcast,
                creator=None,
                number=None,
                episode_url=None,
                date=ep.livedate,
                canceled=False,
                type=podcast.type,
                import_date=datetime.now(),
                stream=ep.streamurl,
                source=cls.shortname,
                source_id=ep.id,
            ))

        return episodes

    @classmethod
    def get_deleted_episodes(cls, date_start):
        return [ep.event_id for ep in hoerapi.get_deleted(dateStart=date_start)]