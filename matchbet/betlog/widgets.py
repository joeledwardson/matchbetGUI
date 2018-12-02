from django_filters import widgets as filter_widgets
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django import forms

css_checkbox_class = 'class-checkbox'
css_select_class = 'class-selector'
css_select_clearable_class = 'class-selector-clearable'
css_date_class = 'class-date-picker'
css_time_class = 'class-time-picker'

# date format is '28/01/04'
date_input = lambda: forms.DateInput(attrs={'class': css_date_class}, format='%d/%m/%y')

class MySelectorWidget(widgets.Select):
    def __init__(self, attrs=None, choices=(), allow_clear=True):
        if not attrs:
            attrs = {}

        # attrs['class'] = ' '.join([css_select_class,
        #                            css_select_clearable_class if allow_clear else ''])
        # attrs['data-live-search'] = 'true'
        attrs['class'] = css_select_class

        super().__init__(attrs=attrs,choices=choices)


class MySelectorWidget_NoClear(MySelectorWidget):
    def __init__(self, attrs=None, choices=()):
        MySelectorWidget.__init__(self, attrs=attrs, choices=choices, allow_clear=False)


# by default no select boolean widget displays 'Unknown' - use blank text for no selection
class FriendlyBooleanWidget(filter_widgets.BooleanWidget):
    def __init__(self, attrs):
        choices = (('', _('')),
                   ('true', _('Yes')),
                   ('false', _('No')))

        attrs['class'] = css_select_class
        # skip BooleanWidget init and go straight to Choice widget super - override choices
        forms.Select.__init__(self, attrs=attrs, choices=choices)

class SliderWidget(widgets.CheckboxInput):
    def __init__(self):
        super().__init__(attrs={'class': 'pls'}) #css_checkbox_class



# custom date time split widget
class DateTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):

        # create two widgets - one for date one for time
        splitWidgets = (
            date_input(),
            forms.TimeInput(format='%H:%M', attrs={'class': css_time_class})
        )
        # call super initialisation with widget list
        super().__init__(splitWidgets, attrs)

    # decompress - add date and time together
    def decompress(self, value):
        if value:
            return [value.date(), value.time()]
        return [None, None]

    # from data dictionary - split widgets e.g. time_0, date_1 into list. return joined string
    def value_from_datadict(self, data, files, name):
        [date, time] = [widget.value_from_datadict(data, files, '{}_{}'.format(name, i))
                        for i, widget in enumerate(self.widgets)]
        return ' '.join([date, time])
