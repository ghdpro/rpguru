"""RPGuru Library models"""

from django.db import models
from django.urls import reverse

from changerequest.models import HistoryModel
from artwork.models import ArtworkModel

from core.models import Language


class Platform(HistoryModel):
    name = models.CharField('name', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    short = models.CharField('short name', max_length=100)
    description = models.TextField(blank=True)
    artwork_active = models.ForeignKey('PlatformArtwork', related_name='platform_artwork', on_delete=models.SET_NULL,
                                       null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self, view='platform:detail'):
        return reverse(view, args=[self.slug])


class PlatformArtwork(ArtworkModel):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)

    ARTWORK_FOLDER = 'platform'
    ARTWORK_SIZES = (150, 300, 600, 900, 1200, 1500, 1800, 2100)

    def sub_folder(self):
        return self.platform.pk


class Franchise(HistoryModel):
    name = models.CharField('name', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Company(HistoryModel):
    name = models.CharField('name', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Genre(HistoryModel):
    name = models.CharField('name', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GameCatalogue(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('franchise_main', 'franchise_side')\
            .prefetch_related('audio', 'developer', 'publisher', 'genre', 'platform')\
            .order_by('-na_date', '-jp_date', '-eu_date')


class Game(HistoryModel):
    class Verdict:
        GOOD = 1
        OKAY = 2
        BAD = 3
        choices = (
            (GOOD, 'Good'),
            (OKAY, 'Okay'),
            (BAD, 'Bad')
        )
    title = models.CharField('title', max_length=250)
    jp_date = models.DateField('Japanese Release Date', null=True, blank=True)
    na_date = models.DateField('North America Release Date', null=True, blank=True)
    eu_date = models.DateField('Europe Release Date', null=True, blank=True)
    audio = models.ManyToManyField(Language)
    franchise_main = models.ForeignKey(Franchise, related_name='main',
                                       null=True, blank=True, on_delete=models.SET_NULL)
    franchise_side = models.ForeignKey(Franchise, related_name='side',
                                       null=True, blank=True, on_delete=models.SET_NULL)
    platform = models.ManyToManyField(Platform)
    developer = models.ManyToManyField(Company, related_name='developer')
    publisher = models.ManyToManyField(Company, related_name='publisher')
    genre = models.ManyToManyField(Genre)
    verdict = models.PositiveSmallIntegerField('verdict', choices=Verdict.choices, default=Verdict.GOOD)
    description = models.TextField(blank=True)
    artwork_active = models.ForeignKey('GameArtwork', related_name='game_artwork', on_delete=models.SET_NULL,
                                       null=True, blank=True, default=None)
    cat = GameCatalogue()

    def __str__(self):
        return self.title


class GameArtwork(ArtworkModel):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    ARTWORK_FOLDER = 'game'
    ARTWORK_SIZES = (150, 300, 600, 900, 1200, 1500, 1800, 2100)

    def sub_folder(self):
        return self.game.pk
