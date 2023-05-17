from django.contrib import admin
from .models import Team
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

class ExportCsvMixin(ImportExportModelAdmin):

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.get_fields()]
        field_names = self.list_filter

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            temp = [getattr(obj, field) for field in field_names]
            members = ",".join([ str(member) for member in getattr(obj,"team_member").all()])
            temp.append(members)
            writer.writerow(temp)

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(Team)
class TeamAdmin(ExportCsvMixin):
    list_display = ("team_name", "team_event","team_size")
    list_filter = ("team_name", "team_event","team_size")
    actions = ["export_as_csv"]


    def admin_action(self, request, queryset):
        pass