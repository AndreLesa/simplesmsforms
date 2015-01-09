from smsform_exceptions import (ChoiceException, InvalidDateException,
    MissingRequiredFieldException)



"""Validators should have a simple signature accepting any number of arguments
to make processing them easier"""

def single_choice_validator(*args, **kwargs):
    """Takes a value and validates that it is atleast one of some number of
    variables"""
    value = kwargs["value"]
    choices = kwargs["choices"]
    if not value in choices:
        raise ChoiceException(
        	"Invalid option '{value}', please select one of: {choices_string}".format(
        		value=value,
        		choices_string=", ".join(choices)))


def multiple_choice_validator(*args, **kwargs):
    """Takes a single value or a list of values and validates that they are all
    part of a set of choices"""
    value = set(kwargs["value"])
    choices = set(kwargs["choices"])
    if not value.issubset(choices):
        raise ChoiceException("Invalid options '{value}', please select one of: {choices_string}".format(
        		value=", ".join(value),
        		choices_string=", ".join(choices)))
