from django.contrib import admin
from .models import Olympiad, Task,  Person, Participation, Score, Country


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortcut', 'olympiad', 'day', 'test',
                    'average_score', 'perfect_scores_for_task', )
    search_fields = ('name', 'shortcut', )
    list_filter = ('olympiad', )

    def average_score(self, obj):
        return str(obj.average_score_for_task()) + "/" + str(obj.perfect_score)


class TaskInline(admin.TabularInline):
    model = Task
    fields = ('name', 'shortcut', 'day', 'test', )
    extra = 0
    show_change_link = True


class ScoreAdmin(admin.ModelAdmin):
    ordering = ('-participation__olympiad__start_date',
                'participation__person',
                'task')
    list_display = ('person', 'task_name',
                    'olympiad', 'result')

    list_filter = ('participation__olympiad', 'task', 'participation__person',)
    search_fields = list_filter

    def task_name(self, obj):
        return obj.task.name + " (" + obj.task.shortcut + ")"

    def person(self, obj):
        return obj.participation.person

    def olympiad(self, obj):
        return obj.participation.olympiad


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0

    # we want to show task only from chosen olympiad
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'task':
            if request._obj is not None:
                kwargs['queryset'] = Task.objects.filter(
                    olympiad=request._obj.olympiad)
        return super(ScoreInline, self) \
            .formfield_for_foreignkey(db_field, request, **kwargs)


class ParticipationAdmin(admin.ModelAdmin):
    inlines = [ScoreInline]
    readonly_fields = ('final_score', 'place', 'award',)
    list_display = ('person', 'olympiad', 'country', 'function', 'place',
                    'final_score', 'award', )
    list_filter = ('olympiad', 'country', 'function', )

    def get_form(self, request, obj=None, **kwargs):
        # we need to pass olympiad for filtering tasks
        request._obj = obj
        return super(ParticipationAdmin, self).get_form(request, obj, **kwargs)


class ParticipationInline(admin.TabularInline):
    model = Participation
    readonly_fields = ('place', 'final_score', 'award',)
    extra = 0
    show_change_link = True


class OlympiadAdmin(admin.ModelAdmin):
    inlines = [TaskInline, ParticipationInline]
    list_display = ('__str__', 'country',
                    'city', 'duration', 'attendees', 'participants_no',)
    search_fields = list_display
    list_filter = ('country', )

    def duration(self, obj):
        return str(obj.start_date) + " - " + str(obj.end_date)

    def attendees(self, obj):
        return len(obj.people())

    def participants_no(self, obj):
        return len(obj.participants())
    participants_no.short_description = "Participants"


class PersonAdmin(admin.ModelAdmin):
    inlines = [ParticipationInline]
    list_display = ('last_name', 'first_name', 'email', 'birth_date', 'sex', )
    search_fields = ('first_name', 'last_name')
    list_display_links = ('first_name', 'last_name', )


class CountryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'code', 'organized_olympiads_no',
                    'participated_olympiads_no', 'first_partcipation',
                    'golden_medals', 'silver_medals', 'bronze_medals')
    inlines = [ParticipationInline]
    readonly_fields = ('organized_olympiads', 'participated_olympiads',
                       'golden_medals', 'silver_medals', 'bronze_medals')

    def participated_olympiads_no(self, obj):
        return len(obj.participated_olympiads())
    participated_olympiads_no.short_description = 'Participations'

    def organized_olympiads_no(self, obj):
        return len(obj.organized_olympiads())
    organized_olympiads_no.short_description = 'Organized olympiads'


admin.site.register(Country, CountryAdmin)
admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Score, ScoreAdmin)
