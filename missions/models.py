from django.db import models
from django.utils.html import format_html
from django.template.defaultfilters import slugify, truncatechars
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from transliterate import translit


class MissionType(models.IntegerChoices):
    DEFAULT = 0, _("Default")
    FLASHBACK = 1, _("Flashback")
    SUBSISTENCE = 2, _("Subsistence")
    STEALTH = 3, _("Stealth")


class MissionChapters(models.IntegerChoices):
    CHAPTER_1 = 0, _("Chapter 1")
    CHAPTER_2 = 2, _("Chapter 2")


class ObjectiveType(models.IntegerChoices):
    PRIMARY = 0, _("Primary")
    SECONDARY = 1, _("Secondary")


class Character(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "ru", reversed=True))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Mission(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=100, verbose_name=_("title"))
    chapter = models.IntegerField(
        default=MissionChapters.CHAPTER_1,
        choices=MissionChapters.choices,
        verbose_name=pgettext_lazy("Mission chapter", "chapter"),
    )
    number = models.IntegerField(default=0, null=False, verbose_name=_("number"))
    slug = models.SlugField(blank=True)
    type = models.IntegerField(
        default=MissionType.DEFAULT, choices=MissionType.choices, verbose_name=_("type")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(
            translit(f"{self.chapter}-${self.number}-{self.title}", "ru", reversed=True)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Mission")
        verbose_name_plural = _("Missions")


class Objective(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField(max_length=2000)
    type = models.IntegerField(
        default=ObjectiveType.PRIMARY, choices=ObjectiveType.choices, null=False
    )
    mission = models.ForeignKey(
        Mission, related_name="objectives", on_delete=models.CASCADE, null=False
    )

    @property
    def text_short(self):
        return truncatechars(self.text, 50)

    def __str__(self):
        return self.title if self.title else "%s %i" % (_("Objective"), self.id)

    class Meta:
        verbose_name = _("Objective")
        verbose_name_plural = _("Objectives")


class ObjectiveImage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="objectives/")
    objective = models.ForeignKey(
        Objective, related_name="images", on_delete=models.CASCADE, null=False
    )

    def image_tag(self):
        return format_html(
            f'<a href="{self.image.url}" target="_blank" alt="{self.image.url}"><img src="{self.image.url}" style="width: 25rem" /></a>'
        )


class Fact(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.TextField(max_length=2000)
    mission = models.ForeignKey(Mission, related_name="facts", on_delete=models.CASCADE)

    @property
    def text_short(self):
        return truncatechars(self.text, 50)

    class Meta:
        verbose_name = _("Fact")
        verbose_name_plural = _("Facts")


class Dialog(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)
    mission = models.ForeignKey(
        Mission, related_name="dialogs", on_delete=models.CASCADE
    )
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    @property
    def text_short(self):
        return truncatechars(self.text, 50)

    def __str__(self):
        return f"{self.mission.title} - {self.character.name} - {self.id}"

    class Meta:
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")
