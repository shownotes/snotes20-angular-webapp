import rules


@rules.predicate
def can_publish_podcast(user, podcast):
    if user.has_perm('snotes20.publish_episode'):
        return True
    if podcast.mums.filter(id=user.id).exists():
        return True
    return False


@rules.predicate
def can_publish_episode(user, episode):
    return can_publish_podcast(user, episode.podcast)

rules.add_perm('o_publish_episode', can_publish_episode)


def can_view_document(user, document):
    return True

rules.add_perm('o_view_document', can_view_document)

def can_edit_document(user, document):
    if not user.is_authenticated():
        return False

    return True

rules.add_perm('o_edit_document', can_edit_document)
