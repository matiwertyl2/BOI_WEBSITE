from django.db import models
from olymp.models import Olympiad
from .validators import validate_ranking
from .controllers import process_ranking


class Ranking(models.Model):
    olympiad = models.ForeignKey(Olympiad)
    ranking = models.FileField(upload_to="rankings")

    def clean(self, *args, **kwargs):
        validate_ranking(self)
        super(Ranking, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Ranking, self).save(*args, **kwargs)
        process_ranking(self)
