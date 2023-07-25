from django.db import models
from django.utils.translation import gettext_lazy as _


class CarrierType(models.IntegerChoices):
    ENDO = 1, _("Endogene")
    XENO = 2, _("Xenogene")


class GeneCategory(models.TextChoices):
    ARCHITE = "ARCHITE", _("Archite")
    SPECIAL_ABILITIES = "SPECIAL_ABILITIES", _("Special abilities")
    HEMOGEN = "HEMOGEN", _("Hemogen")
    HEALTH = "HEALTH", _("Health")
    PSYCHIC = "PSYCHIC", _("Psychic")
    MOVEMENT = "MOVEMENT", _("Movement")
    MOOD = "MOOD", _("Mood")
    TEMPERATURE = "TEMPERATURE", _("Temperature")
    RESISTANCE_AND_SENSITIVITY = "RESISTANCE_AND_SENSITIVITY", _("Resistance and sensitivity")
    VIOLENCE = "VIOLENCE", _("Violence")
    SLEEP = "SLEEP", _("Sleep")
    PAIN = "PAIN", _("Pain")
    REPRODUCTION = "REPRODUCTION", _("Reproduction")
    BEAUTY = "BEAUTY", _("Beauty")
    COSMETIC = "COSMETIC", _("Cosmetic")
    APTITUDES = "APTITUDES", _("Aptitudes")
    DRUGS = "DRUGS", _("Drugs")
    MISCELLANEOUS = "MISCELLANEOUS", _("Miscellaneous")