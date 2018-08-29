"""Module defines validation rules used by the application"""
import re


class Validators:
    """Defines validator functions. can be edited to add more"""

    @staticmethod
    def validate_contact(contact) -> bool:
        """
        Validate contact number. Must be at least 10 digits
        and not more than 13
        :param contact:
        :return:
        """
        if not contact:
            return False

        contact_regex = re.compile("^[0-9]{10,13}$")
        if contact_regex.match(contact):
            return True

        return False

    @staticmethod
    def validate_number(amount) -> bool:
        """
        validate any number. ensure its a number
        :param amount:
        :return:
        """
        if not amount:
            return False
        amount_regex = re.compile("^[0-9]+$")
        try:
            if amount_regex.match(amount) and int(amount) > 0:
                return True
        except TypeError:
            return False
        return False

    @staticmethod
    def validate_email(email) -> bool:
        """
        Validate email address
        :param email:
        :return:
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(email):
            return False
        return True

    @staticmethod
    def validate_password(password, length) -> bool:
        """
        password validator
        :param password:
        :param length:
        :return:
        """
        if not isinstance(length, int):
            raise ValueError("length must be an integer")
        if length > len(password):
            return False
        return password.isalnum()
