import itertools
from smsform_exceptions import SMSFieldException
#SMS Form
class SMSForm(object):

    """The SMS form represents the entire text SMS passed in from the user as a
    represented as a string. It contains all the necessary declarion of the
    expected SMS format, It is the entry point for all SMS processing and
    will initate the validation and processing of a text message.
    USAGE

    class MotherForm(SMSForm):
                    keyword = 'register'

                    first_name = PrefixField(prefix=fn)
                    last_name = PrefixField(prefix=ln)
                    age =  PrefixField(ag)
                    ward = PrefixField(prefix=wd)

                    """
    keyword = ""

    def parse_text(self, text=None):
        if not text:
            text = self.original_text
        """parses the passed in text to return a nice list of the passed in
        fields WITHOUT the form keyword"""
        fields = text.split(" ")
        return [field.strip() for field in fields[1:] if field != ""]

    def bind_fields(self, text_fields):
        """Binds the passed in text fields with the form fields"""
        bound_fields = itertools.izip_longest(
            self.get_fields(),
            text_fields,
            fillvalue=" ")
        return bound_fields

    def get_fields(self):
        return []

    def validate_form(self, bound_fields):
        passed_validation = True
        errors = []
        for sms_field, text in bound_fields:
            try:
                valid_obj = sms_field.process_field(text)
            except SMSFieldException, e:
                errors.append(e)
                passed_validation = False

        return passed_validation, errors

    def process_form(self, original_text):
        parsed_text = self.parse_text()
        bound_fields = self.bind_fields(parsed_text)
        passed_validation, errors = self.validate(bound_fields)

        return passed_validation, bound_fields, errors
