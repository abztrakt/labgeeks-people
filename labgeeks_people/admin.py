from labgeeks_people.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db.models import Count
from forms_builder.forms.forms import EntriesForm
from forms_builder.forms.models import Form, Field, FormEntry, FieldEntry
from forms_builder.forms.settings import CSV_DELIMITER, UPLOAD_ROOT
from forms_builder.forms.settings import USE_SITES, EDITABLE_SLUGS
from forms_builder.forms.utils import now, slugify
from datetime import datetime
from forms_builder.forms.admin import FormAdmin
from django.conf.urls import patterns, url

form_admin_filter_horizontal = ()
form_admin_fieldsets = [
    (None, {"fields": ("title", ("status", "login_required",),
        ("publish_date", "expiry_date",),
        "intro", "button_text", "response")}),
]

if EDITABLE_SLUGS:
    form_admin_fieldsets.append(
            (_("Slug"), {"fields": ("slug",), "classes": ("collapse",)}))

if USE_SITES:
    form_admin_fieldsets.append((_("Sites"), {"fields": ("sites",),
        "classes": ("collapse",)}))
    form_admin_filter_horizontal = ("sites",)


class EmploymentStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(EmploymentStatus, EmploymentStatusAdmin)

class ReviewFieldAdmin(admin.TabularInline):
    model = ReviewField
    exclude = ('slug', )

class ReviewFormAdmin(admin.ModelAdmin):
    formentry_model = ReviewFormEntry
    fieldentry_model = ReviewFieldEntry

    inlines = (ReviewFieldAdmin,)
    list_display = ("title", "status", "publish_date",
                    "expiry_date", "total_entries")
    list_display_links = ("title",)
    list_editable = ("status", "publish_date", "expiry_date")
    list_filter = ("status",)
    filter_horizontal = form_admin_filter_horizontal
    search_fields = ("title", "intro", "response")
    radio_fields = {"status": admin.HORIZONTAL}
    fieldsets = form_admin_fieldsets

    def queryset(self, request):
        qs = super(ReviewFormAdmin, self).queryset(request)
        return qs.annotate(total_entries=Count("entries"))

admin.site.register(ReviewForm, ReviewFormAdmin)


class WorkGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(WorkGroup, WorkGroupAdmin)


class PayGradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(PayGrade, PayGradeAdmin)


class TitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Title, TitleAdmin)
admin.site.register(WageHistory)
admin.site.register(WageChangeReason)


class UWLTReviewWeightsAdmin(admin.ModelAdmin):
    list_display = ('name', 'effective_date',)

admin.site.register(UWLTReviewWeights, UWLTReviewWeightsAdmin)


class UWLTReviewAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'weights',)
    fields = ('weights',)

    def has_add_permission(self, request):
        return False

admin.site.register(UWLTReview, UWLTReviewAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'start_date', 'grad_date', 'supervisor', 'title', 'office',)
    search_fields = ('user', 'title', 'office', 'phone', 'alt_phone',)
    list_filter = ('status', 'start_date', 'grad_date', 'title', 'office',)
    actions = ['change_title', 'change_supervisor']

    class ModifyTitleForm(forms.Form):
        """ The form used by the change_location admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        title = forms.ModelChoiceField(Title.objects)

    class ModifySupervisorForm(forms.Form):
        """ The form used by the change_supervisor admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        supervisor = forms.ModelChoiceField(User.objects)

    def change_title(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyTitleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.title = title
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "title for 1 person."
            else:
                message_bit = "title for %s people." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyTitleForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_title'
        return render_to_response('admin/mod_title.html', {'mod_title_form': form, 'selected_action': selected_action}, context_instance=RequestContext(request, {'title': 'Change Title', }))
    change_title.short_description = "Change title for selected people"

    def change_supervisor(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifySupervisorForm(request.POST)
            if form.is_valid():
                supervisor = form.cleaned_data['supervisor']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.supervisor = supervisor
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "supervisor for 1 person."
            else:
                message_bit = "supervisor for %s people." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifySupervisorForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_supervisor'
        return render_to_response('admin/mod_supervisor.html', {'mod_supervisor_form': form, 'selected_action': selected_action}, context_instance=RequestContext(request, {'title': 'Change Supervisor', }))
    change_supervisor.short_description = "Change supervisor for selected people"
admin.site.register(UserProfile, UserProfileAdmin)

UserAdmin.list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
