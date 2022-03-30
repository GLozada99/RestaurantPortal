from rest_framework.serializers import ValidationError


class Validators():
    """Class to handle validations."""

    @staticmethod
    def validate_greater_than_zero(value):
        """Validate that the entered value is greater than zero."""
        if(value <= 0):
            raise ValidationError('This field must be greater than zero.')
        return value
