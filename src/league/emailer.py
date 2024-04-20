import yagmail
import keyring


class Emailer:
    """A singleton class"""

    sender_address = ""
    """Variable docstring"""
    _sole_instance = None
    """Variable docstring"""

    @classmethod
    def configure(cls, sender_address):
        """sets the class variable as specified."""
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        """return the only instance of this class"""
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        """Note: this is an instance method.
        recipients must be a collection of email addresses
        (not TeamMembers!). subject and message are strings.
        This method prints Sending mail to: {recipient} for each recipient in the recipients list."""
        yag = yagmail.SMTP(self.sender_address,
                           keyring.get_password("emailer", "username"))
        for recipient in recipients:
            yag.send(recipient, subject, message)
            print(f"Sending mail to: {recipient}")


if __name__ == '__main__':
    e = Emailer()
    e.configure('tt4258627@gmail.com')
    e.send_plain_email(['jsr0010@auburn.edu', 'tt4258627@gmail.com'], "Test Email", "Hopefully this works!")