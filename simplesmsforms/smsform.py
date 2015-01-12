import re
import itertools
from smsform_exceptions import SMSFieldException
# SMS Form


class SMSForm(object):

    """The SMS form represents the entire text SMS passed in from the user as a
    represented as a string. It contains all the necessary declarion of the
    expected SMS format, It is the entry point for all SMS processing and
    will initate the validation and processing of a text message.
    USAGE

    class MotherForm(SMSForm):
                    keyword = 'register'

                    first_name = PrefixField(prefixes=fn)
                    last_name = PrefixField(prefixes=ln)
                    age =  PrefixField(ag)
                    ward = PrefixField(prefixes=wd)

                    """
    keyword = ""

    def parse_text(self, text=None):
        if not text:
            text = self.original_text
        """parses the passed in text to return a nice list of the passed in
        fields WITHOUT the form keyword"""
        fields = text.split(" ")
        return [field.strip() for field in fields[1:] if field != ""]

    def bind_fields(self, text_string):
        """Binds the passed in text fields with the form fields and returns
        a dict that looks like:
        {field_name: ("prefix", "value")}
        """

        """
        bound_fields = itertools.izip_longest(
            self.get_fields(),
            text_fields,
            fillvalue=" ")
        """
        bound_fields = ()
        for expected_field in self.get_fields():
            for prefix in expected_field.prefixes:
                prefix_regex = re.compile("{prefix}(?P<{name}>\w*)".format(
                    prefix=prefix,
                    name=expected_field.name
                ), re.IGNORECASE)

                match = prefix_regex.search(text_string)
                if match:
                    bound_field= (expected_field,  (
                        prefix, match.groupdict()[expected_field.name]))
                    bound_fields += (bound_field, )
                    continue
        return bound_fields

    def get_fields(self):
        return []

    def validate_form(self, bound_fields):
        passed_validation = True
        errors = []
        for bound_field in bound_fields:
            try:
                valid_obj = bound_field[0].process_field(bound_field[1][1])
            except SMSFieldException, e:
                errors.append(e)
                passed_validation = False

        return passed_validation, errors

    def process_form(self, original_text):
        bound_fields = self.bind_fields(original_text)
        passed_validation, errors = self.validate_form(bound_fields)

        #The bound fields in here have a structure that binds the actual field
        #functions to the field and prefix. We transform that to (field name, (prefix, text))
        transformed_bound_fields = []
        for bound_field in bound_fields:
            prefix_with_text = (bound_field[1][0], bound_field[1][1])
            transformed_bound_fields.append(
                (bound_field[0].name, prefix_with_text)
                )
        return passed_validation, transformed_bound_fields, errors
