import datetime
import unittest
from smsform_fields import (GenericSMSField, SpecialKeyField, SingleChoiceField,
                        MultiChoiceField, DateField)
from smsform_exceptions import (ChoiceException, InvalidDateException,
    MissingRequiredFieldException)
from smsform import SMSForm


class PersonForm(SMSForm):
    keyword = "REG"
    blank_field = "_"

    first_name = SpecialKeyField(special_key="fn")
    last_name = SpecialKeyField(special_key="ln")
    age = SpecialKeyField(special_key="ag")
    location = SpecialKeyField(special_key="loc")

    def get_fields(self):
        return [self.first_name, self.last_name, self.age, self.location]

# Create your tests here.


class TestSMSForms(unittest.TestCase):

    def setUp(self):
        self.person_form = PersonForm()
        self.person_form.original_text = "REG fnAndre lnLesa ag12 locLusaka"

    def test_parser(self):
        parsed = self.person_form.parse_text()
        self.assertEqual(parsed, ["fnAndre", "lnLesa", "ag12", "locLusaka"])

    def test_fieldbind(self):
        parsed = self.person_form.parse_text()
        form_bound_fields = self.person_form.bind_fields(parsed)

        expected_bound_fields = [
            (self.person_form.first_name, "fnAndre"),
            (self.person_form.last_name,  "lnLesa"),
            (self.person_form.age, "ag12"),
            (self.person_form.location, "locLusaka")
        ]
        self.assertEqual(list(form_bound_fields), expected_bound_fields)


class TestSMSFields(unittest.TestCase):

    def setUp(self):
        self.POSITION_CHOICES = ("clerk", "officer", "supervisor", "director")

    def test_special_key_to_python(self):
        field = SpecialKeyField(special_key="fn")
        data = field.to_python(text="fnandre")
        self.assertEqual(data, "andre")

    def test_multichoice_to_python(self):
        field = MultiChoiceField(
            special_key="pos",
            choices=self.POSITION_CHOICES,
        )
        # test single choice
        data = field.to_python(text="posclerk")
        self.assertEqual(data, ["clerk"])

        # test multiple choices
        data = field.to_python(text="posclerk,officer,supervisor")
        self.assertEqual(data, ["clerk", "officer", "supervisor"])

    def test_bad_date(self):
        field = DateField()

        with self.assertRaises(InvalidDateException):
            python_date = field.to_python("08xxx11xxx14")

    def test_date_to_python(self):
        field = DateField()
        python_date = field.to_python("08/nov/14")

        self.assertEqual(python_date, datetime.datetime(2014, 11, 8))

    def test_for_required_field(self):
        field = SpecialKeyField(special_key="fn")

        with self.assertRaises(MissingRequiredFieldException):
            python_obj = field.to_python("fn")
            field.validate(python_obj)

        with self.assertRaises(MissingRequiredFieldException):
            field.validate("")

    def test_single_choice_validation(self):
        field = SingleChoiceField(choices=self.POSITION_CHOICES)

        expected_msg = "Invalid option 'ceo', please select one of: clerk, officer, supervisor, director"

        with self.assertRaisesRegexp(ChoiceException, expected_msg):
            field.validate('ceo')

    def test_multichoice_validator(self):
        field = MultiChoiceField(choices=self.POSITION_CHOICES)
        # test single INCORRECT choices
        expected_msg = "Invalid options 'ceo, attorney', please select one of: {choices}".format(
            choices=", ".join(set(self.POSITION_CHOICES)))#force into set first
        #because when done in the field itself, the set messes up the ordering
        with self.assertRaisesRegexp(ChoiceException, expected_msg):
            field.validate(["attorney", "ceo"])

if __name__ == '__main__':
    unittest.main()