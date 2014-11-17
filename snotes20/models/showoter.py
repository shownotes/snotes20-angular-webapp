from django.db import models
from django.conf import settings

class Shownoter(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def shown_name(self):
        try:
            return self.user.username
        except:
            return self.name

    def save(self, **kwargs):
        name = self.name

        if name is None:
            try:
                name = self.user.username
            except:
                pass

        if name is None:
            raise Exception("cannot save Shownoter without name and user")

        super(Shownoter, self).save(**kwargs)
