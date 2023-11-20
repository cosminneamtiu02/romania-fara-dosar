class Person:
    def __init__(self, data):
        self._cnp = data.get("cnp")
        self._series = data.get("series")
        self._number = data.get("number")
        self._name = data.get("name")
        self._surname = data.get("surname")
        self._citizenship = data.get("citizenship")
        self._place_of_birth = data.get("place_of_birth")
        self._address = data.get("adress")  # Typo corrected to 'address'
        self._authority = data.get("authority")
        self._date_issued = data.get("date issued")  # Changed to '_date_issued' due to space in the key
        self._valid_until = data.get("valid_until")
        self._sex = data.get("sex")
        self._email = ""
        self._password = ""
        self._phone_number = ""

    @property
    def cnp(self):
        return self._cnp

    @cnp.setter
    def cnp(self, value):
        self._cnp = value

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, value):
        self._series = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def citizenship(self):
        return self._citizenship

    @citizenship.setter
    def citizenship(self, value):
        self._citizenship = value

    @property
    def place_of_birth(self):
        return self._place_of_birth

    @place_of_birth.setter
    def place_of_birth(self, value):
        self._place_of_birth = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def authority(self):
        return self._authority

    @authority.setter
    def authority(self, value):
        self._authority = value

    @property
    def date_issued(self):
        return self._date_issued

    @date_issued.setter
    def date_issued(self, value):
        self._date_issued = value

    @property
    def valid_until(self):
        return self._valid_until

    @valid_until.setter
    def valid_until(self, value):
        self._valid_until = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._email

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def phone_number(self):
        return self._email

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value
