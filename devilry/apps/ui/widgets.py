from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

class DevilryDateWidget(forms.DateTimeInput):
    class Media:
        js = (settings.DEVILRY_STATIC_URL + "/apps/ui/js/datewidget.js",)

    def __init__(self, attrs={}):
        super(DevilryDateWidget, self).__init__(
                attrs = {'class': 'devilry-date', 'size': '11'},
                format = '%Y-%m-%d')

class DevilryTimeWidget(forms.TimeInput):
    class Media:
        js = (settings.DEVILRY_STATIC_URL + "/apps/ui/js/timewidget.js",)

    def __init__(self, attrs={}):
        super(DevilryTimeWidget, self).__init__(
                attrs={'class': 'devilry-time', 'size': '8'},
                format='%H:%M')

class DevilryDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets = [DevilryDateWidget, DevilryTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(
                u'<div class="devilry-datetime">'
                u'<div><span class"devilry-date-label">%s</span> %s</div>' \
                u'<div><span class"devilry-time-label">%s</span> %s</div>' \
                u'</div>' % (
                _('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))


class DevilryMultiSelectFewUsersDb(forms.TextInput):
    class Media:
        js = (settings.DEVILRY_STATIC_URL + "/apps/ui/js/multiSelect_char_user_field.js",)
                
    def __init__(self, attrs={}):
        attrs["size"] = 60
        attrs["class"] = "devilry_multiselect_few"
        super(DevilryMultiSelectFewUsersDb, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        if not isinstance(value, unicode):
            if value:
                qry = User.objects.filter(pk__in=value).all()
                value = u", ".join([u.username for u in qry])
            else:
                value = u""
        return super(DevilryMultiSelectFewUsersDb, self).render(name, value, attrs)


class DevilryMultiSelectFewUsers(forms.TextInput):
    class Media:
        js = (settings.DEVILRY_STATIC_URL + "/apps/ui/js/multiSelect_char_user_field.js",)
                
    def __init__(self, attrs={}):
        attrs["size"] = 60
        attrs["class"] = "devilry_multiselect_few"
        super(DevilryMultiSelectFewUsers, self).__init__(attrs)


class DevilryMultiSelectFewCandidates(forms.TextInput):
    class Media:
        js = (settings.DEVILRY_STATIC_URL + "/apps/ui/js/multiSelect_char_candidates_field.js",)
                
    def __init__(self, attrs={}):
        attrs["size"] = 60
        attrs["class"] = "devilry_multiselect_few"
        super(DevilryMultiSelectFewCandidates, self).__init__(attrs)


MARKITUP_JS  = (
        settings.DEVILRY_MARKITUP_URL + "/markitup/jquery.markitup.js",
        settings.DEVILRY_MARKITUP_URL + "/markitup/sets/rst/rst.js",
        settings.DEVILRY_STATIC_URL + "/apps/ui/js/rstedit_widget.js")
MARKITUP_CSS = (
            settings.DEVILRY_MARKITUP_URL + "/markitup/skins/simple/style.css",
            settings.DEVILRY_MARKITUP_URL + "/markitup/sets/rst/style.css")

class RstEditWidget(forms.Textarea):
    class Media:
        js = MARKITUP_JS
        css = {'all': MARKITUP_CSS}

    def __init__(self, attrs={}):
        if not 'cols' in attrs:
            attrs["cols"] = 70
        if not 'rows' in attrs:
            attrs["rows"] = 35
        attrs["class"] = "devilry_rstedit"
        super(RstEditWidget, self).__init__(attrs)


class DevilryLongNameWidget(forms.TextInput):
    def __init__(self, attrs={}):
        attrs["size"] = 60
        attrs["class"] = "devilry_long_name"
        super(DevilryLongNameWidget, self).__init__(attrs)
