"""RPGuru sitemap"""

from django.contrib.sitemaps import Sitemap

from .models import Platform, Franchise, Company, Genre


def pick_lastmod(obj):
    if obj.lastmod1 and obj.lastmod2 is None:
        return obj.lastmod1
    if obj.lastmod1 is None and obj.lastmod2:
        return obj.lastmod2
    if obj.lastmod1 and obj.lastmod2:
        return obj.lastmod1 if obj.lastmod1 > obj.lastmod2 else obj.lastmod2
    return None


class PlatformSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Platform.objects.raw('''
SELECT attr.*, MAX(game.date_modified) AS lastmod FROM library_platform AS attr
    LEFT JOIN library_game_platform AS through ON (attr.id = through.platform_id)
    LEFT JOIN library_game AS game ON (game.id = through.game_id)
WHERE game.id IS NOT NULL
GROUP BY attr.id
            ''')

    def lastmod(self, obj):
        return obj.lastmod


class FranchiseSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Franchise.objects.raw('''
SELECT attr.*, MAX(g1.date_modified) AS lastmod1, MAX(g2.date_modified) AS lastmod2 FROM library_franchise AS attr
    LEFT JOIN library_game AS g1 ON (attr.id = g1.franchise_main_id)
    LEFT JOIN library_game AS g2 ON (attr.id = g2.franchise_side_id)
WHERE g1.id IS NOT NULL OR g2.id IS NOT NULL
GROUP BY attr.id
            ''')

    def lastmod(self, obj):
        return pick_lastmod(obj)


class CompanySitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Company.objects.raw('''
SELECT attr.*, MAX(g1.date_modified) AS lastmod1, MAX(g2.date_modified) AS lastmod2 FROM library_company AS attr
    LEFT JOIN library_game_developer as t1 ON (attr.id = t1.company_id)
    LEFT JOIN library_game AS g1 ON (g1.id = t1.game_id)
    LEFT JOIN library_game_publisher as t2 ON (attr.id = t2.company_id)
    LEFT JOIN library_game AS g2 ON (g2.id = t2.game_id)
WHERE g1.id IS NOT NULL OR g2.id IS NOT NULL
GROUP BY attr.id
            ''')

    def lastmod(self, obj):
        return pick_lastmod(obj)


class GenreSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Genre.objects.raw('''
SELECT attr.*, MAX(game.date_modified) AS lastmod FROM library_genre AS attr
    LEFT JOIN library_game_genre AS through ON (attr.id = through.genre_id)
    LEFT JOIN library_game AS game ON (game.id = through.game_id)
WHERE game.id IS NOT NULL
GROUP BY attr.id
            ''')

    def lastmod(self, obj):
        return obj.lastmod


sitemaps = {
    'platform': PlatformSitemap,
    'series': FranchiseSitemap,
    'company': CompanySitemap,
    'genre': GenreSitemap,
}
