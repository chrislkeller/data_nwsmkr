from django.contrib import admin
from .models import Event
from django.utils.timezone import utc, localtime
import logging

logger = logging.getLogger("accountability_tracker")

class EventAdmin(admin.ModelAdmin):

    fields = [
        "created_at",
        "event_type",
        "event_notes",
    ]

    list_display = (
        "created_at",
        "event_type",
        "event_notes",
    )

    list_per_page = 15

    list_filter = (
        "event_type",
        "event_notes",
    )

    ordering = (
        "created_at",
    )

    search_fields = (
        "event_type",
        "event_notes",
    )

    save_on_top = True

admin.site.register(Event, EventAdmin)
