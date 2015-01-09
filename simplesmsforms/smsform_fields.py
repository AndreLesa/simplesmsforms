import datetime

from smsform_exceptions import (SMSFieldException, ChoiceException, InvalidDateException,
    MissingRequiredFieldException)
from smsform_validators import multiple_choice_validator, single_choice_validator

# SMS FIELD
class GenericSMSField(object):
    required = True
    empty_values = [None, [], ""]

    def __init__(self, *args, **kwargs):
    	self.validators = kwargs.get('validators') or []

    def to_python(self, text):
        """Convert the passed in text to a valid python object, any special
        conversions from the passed in text to a valid python object should
        happen here."""
        return text.strip().lower()

    def validate(self, value):
        # check to see if the field is required and present
        if self.required and value in self.empty_values:
            raise MissingRequiredFieldException(self.__class__.__name__)

        for validator in self.validators:
        	try:
        		validator(value=value, choices=self.choices)
        	except SMSFieldException, e:
        		raise
        return True

    def process_field(self, text):
        try:
        	python_obj = self.to_python(text)
        except SMSFieldException:
        	#Do something
        	raise

        try:
        	python_obj = self.validate(python_obj)
        except SMSFieldException:
        	#Do something
     		raise

     	return python_obj


# SMSFields
class PrefixField(GenericSMSField):

    """This field is for the special fields that have a first letter followed by
    the actual data. This class just strips out that first letter"""

    def __init__(self, *args, **kwargs):
        super(PrefixField, self).__init__(*args, **kwargs)
        self.prefix = kwargs.get("prefix") or ""

    def to_python(self, text):
        """The returned field should be either an ID or an NRC. Nicely cleaned
        """
        text = super(PrefixField, self).to_python(text)
        if text.startswith(self.prefix):
            return text[len(self.prefix):]

        return text


class MultiChoiceField(PrefixField):

    def __init__(self, choices, choice_divider=",", *args, **kwargs):
        self.choice_divider = choice_divider
        self.choices = choices
        super(MultiChoiceField, self).__init__(*args, **kwargs)
        self.validators.append(multiple_choice_validator)

    def to_python(self, text):
        text = super(MultiChoiceField, self).to_python(text)
        return text.split(self.choice_divider)


class SingleChoiceField(PrefixField):
    def __init__(self, choices, *args, **kwargs):
        super(SingleChoiceField, self).__init__(*args, **kwargs)
        self.choices = choices
        self.validators.append(single_choice_validator)


class DateField(GenericSMSField):

    def __init__(self, *args, **kwargs):
        date_formats = kwargs.get("date_formats", None) or ["%d/%b/%y"]
        super(DateField, self).__init__(*args, **kwargs)
        self.date_formats = date_formats

    def to_python(self, date_string):
        python_date = None
        for date_format in self.date_formats:
            try:
                python_date = datetime.datetime.strptime(
                    date_string, date_format)
            except ValueError:
                continue
            else:
                break

        if not python_date:
            raise InvalidDateException(
                "Date not recognized, please use the format: day/Month/Year"
            )

        return python_date
