"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2020, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.6.0/LICENSE"
__version__ = "1.6.0"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class Usage(models.Model):
    """
    Base usage model
    """
    text_unit = models.ForeignKey('document.TextUnit', db_index=True, on_delete=CASCADE)
    document = models.ForeignKey('document.Document', null=True, blank=True, db_index=True, on_delete=CASCADE)
    # document_name = models.CharField(max_length=1024, db_index=True, null=True)
    project = models.ForeignKey('project.Project', null=True, blank=True, db_index=True, on_delete=CASCADE)
    # project_name = models.CharField(max_length=100, db_index=True, null=True)
    count = models.IntegerField(null=False, default=0, db_index=True)

    class Meta:
        abstract = True


class ProjectUsage(models.Model):
    project = models.ForeignKey('project.Project', db_index=True, on_delete=DO_NOTHING)
    count = models.IntegerField(null=False, default=0, db_index=True)

    class Meta:
        abstract = True
        managed = False


class DocumentUsage(models.Model):
    """
    Base usage model on document level
    """
    document = models.ForeignKey('document.Document', db_index=True, on_delete=CASCADE)
    count = models.IntegerField(null=False, default=0, db_index=True)

    class Meta:
        abstract = True


class TermManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        # to update global cached terms if they are loaded via fixtures
        super().bulk_create(objs, **kwargs)
        from apps.extract.dict_data_cache import cache_term_stems
        cache_term_stems()


class Term(models.Model):
    """
    Legal term/dictionary entry
    """
    term = models.CharField(max_length=1024, db_index=True)
    source = models.CharField(max_length=1024, db_index=True, null=True)
    definition_url = models.CharField(max_length=1024, null=True)
    objects = TermManager()

    class Meta:
        ordering = ('term', 'source')

    def __str__(self):
        return "Term (term={0}, source={1})" \
            .format(self.term, self.source)


@receiver(post_save, sender=Term)
def cache_term(instance, **kwargs):
    from apps.extract.dict_data_cache import cache_term_stems
    # update global cache
    cache_term_stems()
    for project_id in instance.projecttermconfiguration_set.values_list('project_id', flat=True):
        # update project-term caches
        cache_term_stems(project_id)


@receiver(pre_delete, sender=Term)
def delete_term_recache_projecttermconfig(instance, **kwargs):
    # update project-term caches
    for config in instance.projecttermconfiguration_set.all():
        config.terms.remove(instance)
        # this activates ProjectTermConfiguration m2m_changed signal where deleted term is handled


@receiver(post_delete, sender=Term)
def delete_cached_term(instance, **kwargs):
    # update global cache
    from apps.extract.dict_data_cache import cache_term_stems
    cache_term_stems()


class TermUsage(Usage):
    """
    Legal term/dictionary usage
    """
    term = models.ForeignKey(Term, db_index=True, on_delete=CASCADE)

    class Meta:
        unique_together = (("text_unit", "term"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ['-count']

    def __str__(self):
        return "DocumentTermUsage (term={0}, text_unit={1}, count={2})" \
            .format(self.term, self.text_unit, self.count)


class DocumentTermUsage(DocumentUsage):
    """
    Legal term/dictionary usage
    """
    term = models.ForeignKey(Term, db_index=True, on_delete=CASCADE)

    class Meta:
        unique_together = (("document", "term"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ['-count']

    def __str__(self):
        return "TermUsage (term={0}, document={1}, count={2})" \
            .format(self.term, self.document, self.count)


class ProjectTermUsage(ProjectUsage):
    # to be filled with a trigger

    term = models.OneToOneField(Term, db_index=True, on_delete=DO_NOTHING, primary_key=True)


class GeoEntity(models.Model):
    """
    Entity, e.g., geographic or political
    """
    entity_id = models.PositiveSmallIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=1024, db_index=True)
    priority = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=1024, db_index=True)
    description = models.TextField(null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        unique_together = (("name", "category"),)
        verbose_name_plural = 'Geo Entities'
        ordering = ('name', 'entity_id', 'category')

    def __str__(self):
        return "GeoEntity (id={0}, name={1}, category={2}" \
            .format(self.entity_id, self.name, self.category)


class GeoRelation(models.Model):
    """
    GeoPolitical Entity relation
    """
    entity_a = models.ForeignKey(GeoEntity, db_index=True, related_name="entity_a_set", on_delete=CASCADE)
    entity_b = models.ForeignKey(GeoEntity, db_index=True, related_name="entity_b_set", on_delete=CASCADE)
    relation_type = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return "GeoRelation (entity_a={0}, entity_b={1}, type={2}" \
            .format(self.entity_a, self.entity_b, self.relation_type)


class GeoAlias(models.Model):
    """
    GeoPolitical aliases
    """
    entity = models.ForeignKey(GeoEntity, db_index=True, on_delete=CASCADE)
    locale = models.CharField(max_length=10, default='en-us', db_index=True)
    alias = models.CharField(max_length=1024, db_index=True)
    type = models.CharField(max_length=1024, default='abbreviation', db_index=True)

    def __str__(self):
        return "GeoAlias (alias={0}, type={1}, entity={2}" \
            .format(self.alias, self.type, self.entity)


class GeoEntityUsage(Usage):
    """
    Geo Entity usage
    """
    entity = models.ForeignKey(GeoEntity, db_index=True, on_delete=CASCADE)

    class Meta:
        unique_together = (("text_unit", "entity"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "GeoEntityUsage (entity={0}, text_unit={1}, count={2})" \
            .format(self.entity, self.text_unit, self.count)


class ProjectGeoEntityUsage(ProjectUsage):
    # to be filled with a trigger

    entity = models.OneToOneField(GeoEntity, db_index=True, on_delete=DO_NOTHING, primary_key=True)


class GeoAliasUsage(Usage):
    """
    Geo Alias usage
    """
    alias = models.ForeignKey(GeoAlias, db_index=True, on_delete=CASCADE)

    class Meta:
        unique_together = (("text_unit", "alias"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "GeoAliasUsage (alias={0}, text_unit={1}, count={2})" \
            .format(self.alias, self.text_unit, self.count)


class Party(models.Model):
    """
    Party, e.g., person or company
    """
    name = models.CharField(max_length=1024, db_index=True)
    type = models.CharField(max_length=1024, blank=True, null=True, db_index=True)
    type_abbr = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    type_label = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    type_description = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    description = models.TextField(null=True)

    class Meta:
        unique_together = (("name", "type_abbr"),)
        verbose_name_plural = 'Parties'
        ordering = ('name', 'type')

    def __str__(self):
        return "Party (name={0}, type={1}, description={2}" \
            .format(self.name, self.type, self.description)


class PartyUsage(Usage):
    """
    Party usage
    """
    party = models.ForeignKey(Party, db_index=True, on_delete=CASCADE)
    role = models.CharField(max_length=1024, db_index=True, blank=True, null=True)

    class Meta:
        unique_together = (("text_unit", "party"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "PartyUsage (party={0}, role={1}, text_unit={2})" \
            .format(self.party, self.role, self.text_unit)


class ProjectPartyUsage(ProjectUsage):
    # to be filled with a trigger

    party = models.OneToOneField(Party, db_index=True, on_delete=DO_NOTHING, primary_key=True)


class DateUsage(Usage):
    """
    Date usage
    """
    ED = 'exact_date'
    WD = 'without_day'
    WY = 'without_year'
    FORMAT_CHOICES = (
        (ED, ED),
        (WD, WD),
        (WY, WY)
    )

    date = models.DateField(db_index=True)
    date_str = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    format = models.CharField(max_length=30, choices=FORMAT_CHOICES, default=ED, db_index=True)

    class Meta:
        unique_together = (("text_unit", "date"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "DateUsage (date={0}, text_unit={1})" \
            .format(self.date, self.text_unit)


class DefinitionUsage(Usage):
    """
    Definition usage
    """
    definition = models.TextField(db_index=True)
    definition_str = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (("text_unit", "definition"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "DefinitionUsage (definition={0}, text_unit={1})" \
            .format(self.definition, self.text_unit)


class DocumentDefinitionUsage(DocumentUsage):
    """
    Definition usage
    """
    definition = models.TextField(db_index=True)

    class Meta:
        unique_together = (("document", "definition"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "DefinitionUsage (definition={0}, document={1})" \
            .format(self.definition, self.document)


class ProjectDefinitionUsage(ProjectUsage):
    # to be filled with a trigger

    definition = models.TextField(db_index=True, unique=True, primary_key=True)


class CopyrightUsage(Usage):
    """
    Copyright usage
    """
    year = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    copyright_str = models.CharField(max_length=200)

    class Meta:
        unique_together = (("text_unit", "name", "year"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "CopyrightUsage (copyright={0}, text_unit={1})" \
            .format(self.copyright_str, self.text_unit)


class TrademarkUsage(Usage):
    """
    Trademark usage
    """
    trademark = models.CharField(max_length=200, db_index=True)

    class Meta:
        unique_together = (("text_unit", "trademark"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "TrademarkUsage (trademark={0}, text_unit={1})" \
            .format(self.trademark, self.text_unit)


class UrlUsage(Usage):
    """
    Url usage
    """
    source_url = models.CharField(max_length=1000, db_index=True)

    class Meta:
        unique_together = (("text_unit", "source_url"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "UrlUsage (source_url={0}, text_unit={1})" \
            .format(self.source_url, self.text_unit)


class Court(models.Model):
    """
    Courts
    """
    court_id = models.IntegerField(default=0)
    type = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=1024, db_index=True)
    level = models.CharField(max_length=30, db_index=True, blank=True)
    jurisdiction = models.CharField(max_length=30, db_index=True, blank=True)
    alias = models.CharField(max_length=1024, db_index=True, blank=True)

    class Meta:
        ordering = ('court_id',)

    def __str__(self):
        return "Court (id={0}, name={1}, type={2}, alias={3})" \
            .format(self.court_id, self.name, self.type, self.alias)


class CourtUsage(Usage):
    """
    Court usage
    """
    court = models.ForeignKey(Court, db_index=True, on_delete=CASCADE)

    class Meta:
        unique_together = (("text_unit", "court"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "CourtUsage (court={0}, text_unit={1})" \
            .format(self.court.name, self.text_unit)


class RegulationUsage(Usage):
    """
    Regulation usage
    """
    entity = models.ForeignKey(GeoEntity, null=True, blank=True, db_index=True, on_delete=CASCADE)
    regulation_type = models.CharField(max_length=128, db_index=True)
    regulation_name = models.CharField(max_length=1024, db_index=True)

    class Meta:
        unique_together = (("text_unit", "entity", "regulation_type"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "RegulationUsage (regulation_name={0}, text_unit={1})" \
            .format(self.regulation_name, self.text_unit)


class BaseAmountUsage(Usage):
    """
    Base Amount usage model
    """
    amount = models.FloatField(blank=True, null=True, db_index=True)
    amount_str = models.CharField(max_length=300, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-amount',)

    def save(self, *args, **kwargs):
        if self.amount_str:
            self.amount_str = self.amount_str[:300]
        super().save(*args, **kwargs)


class AmountUsage(BaseAmountUsage):
    """
    Amount usage
    """

    def __str__(self):
        return "AmountUsage (amount={})" \
            .format(self.amount)


class CurrencyUsage(BaseAmountUsage):
    """
    Currency usage
    """
    usage_type = models.CharField(max_length=1024, db_index=True)
    currency = models.CharField(max_length=1024, db_index=True)

    class Meta:
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-amount',)

    def __str__(self):
        return "CurrencyUsage (usage_type={0}, currency={1}), amount={2})" \
            .format(self.usage_type, self.currency, self.amount)


class DistanceUsage(BaseAmountUsage):
    """
    Distance usage
    """
    distance_type = models.CharField(max_length=1024, db_index=True)

    class Meta:
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-amount',)

    def __str__(self):
        return "DistanceUsage (distance_type={0}, amount={1})" \
            .format(self.distance_type, self.amount)


class RatioUsage(BaseAmountUsage):
    """
    Ratio usage
    """
    amount2 = models.FloatField(blank=True, null=True, db_index=True)
    total = models.FloatField(blank=True, null=True, db_index=True)

    class Meta:
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-amount',)

    def __str__(self):
        return "RatioUsage ({0} : {1})" \
            .format(self.amount, self.amount2)


class PercentUsage(BaseAmountUsage):
    """
    Percent usage
    """
    unit_type = models.CharField(max_length=1024, db_index=True)
    total = models.FloatField(blank=True, null=True, db_index=True)

    class Meta:
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-amount',)

    def __str__(self):
        return "PercentUsage (unit_type={0}, amount={1})" \
            .format(self.unit_type, self.amount)


class DateDurationUsage(BaseAmountUsage):
    """
    Date Duration usage
    """
    duration_type = models.CharField(max_length=1024, blank=True, null=True, db_index=True)
    duration_days = models.FloatField(blank=True, null=True, db_index=True)

    class Meta:
        unique_together = (("text_unit", "amount_str"),)
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('amount',)

    def __str__(self):
        return "DateDurationUsage (amount_str={0}, text_unit={1})" \
            .format(self.amount_str, self.text_unit)


class CitationUsage(Usage):
    """
    Citation usage
    """
    volume = models.PositiveIntegerField(db_index=True)
    reporter = models.CharField(max_length=1024, db_index=True)
    reporter_full_name = models.CharField(max_length=1024, blank=True, null=True, db_index=True)
    page = models.PositiveIntegerField(db_index=True)
    page2 = models.CharField(max_length=1024, blank=True, null=True, db_index=True)
    court = models.CharField(max_length=1024, blank=True, null=True, db_index=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True, db_index=True)
    citation_str = models.CharField(max_length=1024, db_index=True)

    class Meta:
        # Warning: ordering on non-indexed fields or on multiple fields in joined tables
        # catastrophically slows down queries on large tables
        ordering = ('-count',)

    def __str__(self):
        return "CitationUsage (citation_str={0}, text_unit={1})" \
            .format(self.citation_str, self.text_unit)
