from app.helpers.helpers import validate_email

class TestValidateEmail:
    def test_validate_email_with_valid_email(self):
        assert validate_email("test@email.com") == True

    def test_validate_email_with_invalid_email(self):
        assert validate_email("testemail.com") == False

    def test_validate_email_with_empty_string(self):
        assert validate_email("") == False
