import rules


@rules.predicate
def can_publish_podcast(user, podcast):
    if user.has_perm('publish_episode'):
        return True
    if podcast.mums.filter(id=user.id).exists():
        return True
    return False


@rules.predicate
def can_publish_episode(user, episode):
    return can_publish_podcast(user, episode.podcast)


rules.add_perm('o_publish_episode', can_publish_episode)
