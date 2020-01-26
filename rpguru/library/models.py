"""RPGuru Library models"""

from django.db import models
from django.urls import reverse

from changerequest.models import HistoryModel

from ..core.models import Language


class Platform(HistoryModel):
    name = models.CharField('name', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    short = models.CharField('short name', max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, view='platform'):
        return reverse(view, args=[self.slug])


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

    def __str__(self):
        return self.title
