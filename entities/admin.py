from django.contrib import admin
from django.contrib.auth.backends import UserModel
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import *
import csv
from django.urls import path
# from django.contrib


# Register your models here.
# admin.site.register(Hero)
# admin.site.register(Entity)
# admin.site.register(Origin)
# admin.site.register(Villain)
# admin.site.register(Category)
# admin.site.register(UserModel)

# admin.site.register(FlexCategory)
# class VillainInline(admin.StackedInline):
#     model = Villain

class HeroAcquaintanceInline(admin.TabularInline):
    model = HeroAcquaintance

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # inlines = [VillainInline]
    inlines = [HeroAcquaintanceInline]


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name", "hero_count", "villain_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hero_count=Count("hero", distinct=True),
            _villain_count=Count("villain", distinct=True),
        )
        return queryset


    # Removing add button for a origin model
    # def has_add_permission(self, request):
    #     return False

    def hero_count(self, obj):
        return obj._hero_count

    def villain_count(self, obj):
        return obj._villain_count

    hero_count.admin_order_field = '_hero_count'
    villain_count.admin_order_field = '_villain_count'



class IsVeryBenevolentFilter(admin.SimpleListFilter):
    title = 'is_very_benevolent'
    parameter_name = 'is_very_benevolent'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(benevolence_factor__gt=75)
        elif value == 'No':
            return queryset.exclude(benevolence_factor__gt=75)
        return queryset


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

# actions = ["mark_immortal"]

# from django.forms import forms
# from django.forms import ModelForm,CharField, forms
from django import forms

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


# class HeroAcquaintanceInline(admin.TabularInline):
#     model = HeroAcquaintance



# from django.forms import ModelForm,CharField, forms
# class HeroForm(forms.ModelForm):
#     category_name = forms.CharField()
#
#     class Meta:
#         model = Hero
#         exclude = ["category"]

import sys


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "Category: {}".format(obj.name)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin,ExportCsvMixin):
    # form = HeroForm
    # inlines = [HeroAcquaintanceInline]
    readonly_fields = ["father","mother","spouse"]
    # list_per_page = 1
    # list_per_page = sys.maxsize
    # date_hierarchy = 'added_on'

    change_list_template = "heroes_changelist.html"
    list_display = ("name", "is_immortal", "category", "origin", "is_very_benevolent","children_display")
    # list_filter = ("is_immortal", "category", "origin",)
    list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)

    # actions = ["mark_immortal"]

    # def mark_immortal(self, request, queryset):
    #     queryset.update(is_immortal=True)
    # inlines = [HeroAcquaintanceInline]



    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ["name", "category"]
    #     else:
    #         return []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return CategoryChoiceField(queryset=Category.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


    """ADDING IMAGE FIELD INTO THE HERO MODEL
    
    # readonly_fields = [..., "headshot_image"]

    def headshot_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.headshot.url,
            width=obj.headshot.width,
            height=obj.headshot.height,
            )
    )
    """

    """
    --Associate model with current user while saving--
    
    exclude = ['added_by', ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
        
    """

    # def save_model(self, request, obj, form, change):
    #     category_name = form.cleaned_data["category_name"]
    #     category, _ = Category.objects.get_or_create(name=category_name)
    #     obj.category = category
    #     super().save_model(request, obj, form, change)

    def children_display(self, obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name),
                        args=(child.pk,)),
                child.name)
            for child in obj.children.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # path('immortal/', self.set_immortal),
            # path('mortal/', self.set_mortal),
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls


    def children_display(self, obj):
        return ", ".join([
            child.name for child in obj.children.all()
        ])

    children_display.short_description = "Children"

    """
    Addiing Buttons in hero admin list page

    # def set_immortal(self, request):
        self.model.objects.all().update(is_immortal=True)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect("../")

    def set_mortal(self, request):
        self.model.objects.all().update(is_immortal=False)
        self.message_user(request, "All heroes are now mortal")
        return HttpResponseRedirect("../")
    """

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def is_very_benevolent(self, obj):
        return obj.benevolence_factor > 75

    is_very_benevolent.boolean = True

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        pass

    export_as_csv.short_description = "Export Selected"

    # Removing add button for hero model
    # def has_add_permission(self, request):
    #     return False

    # Removing delete button for hero model
    # def has_delete_permission(self, request, obj=None):
    #     return False

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin, ExportCsvMixin):
    # readonly_fields = ["malevolence_factor"]
    list_display = ("name", "category", "origin")
    change_form_template = "change_form.html"
    actions = ["export_as_csv"]

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            matching_names_except_this.delete()
            obj.is_unique = True
            obj.save()
            self.message_user(request, "This villain is now unique")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)



@admin.register(HeroProxy)
class HeroProxyAdmin(admin.ModelAdmin):
    readonly_fields = ("name","is_immortal","category","origin")


# @admin.register(AllEntity)
# class AllEntityAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
