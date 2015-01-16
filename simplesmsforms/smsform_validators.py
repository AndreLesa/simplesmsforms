from smsform_exceptions import (ChoiceException, InvalidDateException,
    MissingRequiredFieldException)



"""Validators should have a simple signature accepting any number of arguments
to make processing them easier"""


def multiple_choice_validator(*args, **kwargs):
    """Takes a single value or a list of values and validates that they are all
    part of a set of choices"""
    value = set(kwargs["value"])
    choices = set(kwargs["choices"])
    if not value.issubset(choices):
        raise ChoiceException("Invalid option '{value}', please select one of: {choices_string}".format(
                value=", ".join(value),
                choices_string=", ".join(choices)))

def single_choice_validator(*args, **kwargs):
    """Takes a value and validates that it is atleast one of some number of
    variables"""
    multiple_choice_validator(*args, **kwargs)

    value = kwargs.get("value")
    choices = kwargs.get("choices")
    if len(value) > 1:
        raise ChoiceException("Please select only one value out of {choices_string}".format(
            choices_string=", ".join(choices)))