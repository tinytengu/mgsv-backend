from django.contrib import admin

from .models import *


class MissionObjectiveAdminInline(admin.StackedInline):
    model = Objective
    extra = 0
    show_change_link = True
    classes = ("collapse",)


class MissionFactAdminInline(admin.StackedInline):
    model = Fact
    extra = 0
    show_change_link = True
    classes = ("collapse",)


class MissionDialogAdminInline(admin.StackedInline):
    model = Dialog
    extra = 0
    show_change_link = True
    classes = ("collapse",)


class ObjectiveImageAdminInline(admin.StackedInline):
    model = ObjectiveImage
    extra = 0
    show_change_link = True
    fields = ("id", "image", "objective", "image_tag")
    readonly_fields = ("image_tag",)
    classes = ("collapse",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    readonly_fields = ("slug",)
    search_fields = ("name", "slug")
    ordering = ("id",)


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id", "chapter", "number", "title", "slug", "type")
    list_filter = ("chapter", "type")
    search_fields = ("chapter", "title", "slug")
    readonly_fields = ("slug",)
    ordering = ("id",)
    save_on_top = True
    inlines = (
        MissionObjectiveAdminInline,
        MissionFactAdminInline,
        MissionDialogAdminInline,
    )


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ("id", "mission", "title", "text_short", "type")
    list_filter = ("type", "mission__title")
    search_fields = ("mission__title", "title", "text")
    ordering = ("id",)
    inlines = (ObjectiveImageAdminInline,)


@admin.register(ObjectiveImage)
class ObjectiveImageAdmin(admin.ModelAdmin):
    list_display = ("id", "objective", "image")
    list_filter = ("objective",)
    search_fields = ("objective__title", "image")
    readonly_fields = ("image_tag",)
    ordering = ("id",)


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ("id", "text_short")
    list_filter = ("mission",)
    search_fields = ("text", "mission__title")
    ordering = ("id",)


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "character", "text_short", "mission")
    list_filter = ("mission",)
    search_fields = ("title", "text", "character__name", "mission__title")
    ordering = ("id",)
    raw_id_fields = ("character",)
