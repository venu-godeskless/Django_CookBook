from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.admin import AdminSite
from .models import *
# Register your models here.

# admin.site.register(EventVillain)
# admin.site.register(Epic)
# admin.site.register(EventHero)
# admin.site.register(Event)


from django.contrib.admin import AdminSite
class EventAdminSite(AdminSite):
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"

event_admin_site = EventAdminSite(name='event_admin')

# @admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'epic', 'years_ago')
    class Meta:
        model = Event


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'slug')
    prepopulated_fields = {"slug": ("headline",)}
    class Meta:
        model = Article

# event_admin_site.register(Epic)
# event_admin_site.register(Event)
# event_admin_site.register(EventHero)
# event_admin_site.register(EventVillain)
# event_admin_site.register(Article)
# event_admin_site.register(UserParent)
# event_admin_site.register(ColumnName)
# event_admin_site.register(TempUser)
# event_admin_site.register(EventAdminSite)
# event_admin_site.register(EventAdmin)
# event_admin_site.register(ArticleAdmin)



"""
from django.contrib import admin


from django.contrib.auth.models import User, Group
admin.site.unregister(User)
admin.site.unregister(Group)



from django.contrib.admin import AdminSite
from .models import Epic, Event, EventHero, EventVillain


class EventAdminSite(AdminSite):
    site_header = "UMSRA Events Admin2"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"


    def get_app_list(self, request):
        
        # Return a sorted list of all the installed apps that have been registered in this site.
       
        ordering = {
            "Event heros": 1,
            "Event villains": 2,
            "Epics": 3,
            "Events": 4
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

event_admin_site = EventAdminSite(name='event_admin')


event_admin_site.register(Epic)
event_admin_site.register(Event)
event_admin_site.register(EventHero)
event_admin_site.register(EventVillain)
"""