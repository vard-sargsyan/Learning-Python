import re
from datetime import datetime


class Employee:
    date_formats = {'%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y',
                    '%d.%m.%y', '%d/%m/%y', '%d-%m-%y'}
    emails = set()
    teams = []

    def __init__(self, first_name, last_name, join_date, salary, gender,
                 leave_date=None, phone_number=None, trial_passed=False):
        self._first_name = None    # To prevent deletion / leaving empty
        self.first_name = first_name
        self._last_name = None    # To prevent deletion / leaving empty
        self.last_name = last_name
        self._phone_number = None
        self.phone_number = phone_number
        self._email_first = None
        self._email_last = None
        self.work_email = f'{first_name.lower()}.{self.last_name.lower()}@company.com'
        self._trial_passed = None
        self.trial_passed = trial_passed
        self._join_date = None
        self.join_date = join_date
        self._leave_date = None
        self.leave_date = leave_date
        self._salary = None
        self.salary = salary
        self._gender = None
        self.gender = gender
        
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, str):
            self._first_name = value
        else:
            raise ValueError('first_name should be a string.')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, str):
            self._last_name = value
        else:
            raise ValueError('last_name should be a string.')

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @full_name.setter
    def full_name(self, value):
        if not isinstance(value, str):
            raise TypeError('full_name should be a string consisting of two words.')
        name = value.split()
        if len(name) != 2:
            raise ValueError('full_name should consist of two words.')
        else:
            self.first_name, self.last_name = name

    @staticmethod
    def is_phone_number(phone_number):
        pattern = r'^0(33|41|43|44|49|55|77|91|93|94|95|96|98|99) ([0-9]{2} [0-9]{2} [0-9]{2})$'
        if re.search(pattern, phone_number):
            return True
        else:
            return False

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('phone_number should be either a string in "0xx xx xx xx" format or None.')
        if value is None or self.is_phone_number(value):
            self._phone_number = value
        else:
            raise ValueError('Not a valid phone number.')

    @staticmethod
    def is_corporate_email(email):
        pattern = r'^[a-z]+\.[a-z]+@company.com$'
        if re.search(pattern, email):
            return True
        else:
            return False

    @property
    def work_email(self):
        if self._email_first is None or self._email_last is None:
            return None
        else:
            return f'{self._email_first.lower()}.{self._email_last.lower()}@company.com'

    @work_email.setter
    def work_email(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('work_email should be either a valid email ending @company.com or None.')
        if value is not None and not self.is_corporate_email(value):
            raise ValueError('Invalid email address.')
        if value not in self.__class__.emails:
            name = value.split('@')
            self._email_first, self._email_last = name[0].split('.')
            self.__class__.emails.add(value)
        else:
            self._email_first = None
            self._email_last = None
            print(f'work_email {value} already exists. Please enter another one manually.')

    @property
    def trial_passed(self):
        return self._trial_passed

    @trial_passed.setter
    def trial_passed(self, value):
        if isinstance(value, bool):
            self._trial_passed = value
        else:
            raise ValueError('trial_passed should be either True or False.')

    @property
    def join_date(self):
        return self._join_date

    @join_date.setter
    def join_date(self, value):
        for format in self.__class__.date_formats:
            try:
                dt = datetime.strptime(value, format)
                break
            except (ValueError, TypeError):
                continue
        else:
            raise ValueError('Date should be a string in "dd.mm.yyyy" format.')

        '''Not to allow to enter join_dates before 2000 (let's assume this is
        when the company was established) or dates too much into future'''
        if dt < datetime(2000, 1, 1) or (dt - datetime.now()).days > 30:
            raise ValueError('Date <2000 or in more than a month not allowed.')
        else:
            self._join_date = dt

    @property
    def leave_date(self):
        return self._leave_date

    @leave_date.setter
    def leave_date(self, value):
        if value is None:
            self._leave_date = value
            return
        for format in self.__class__.date_formats:
            try:
                dt = datetime.strptime(value, format)
                break
            except (ValueError, TypeError):
                continue
        else:
            raise ValueError('Not a valid date.')

        if dt < self.join_date:
            raise ValueError('leave_date cannot come before join_date.')
        else:
            self._leave_date = dt

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        try:
            if value < 10000 or value > 5000000:
                raise ValueError('Not a valid number for salary.')
            else:
                self._salary = value
        except TypeError:
            raise TypeError('Salary should be a number')

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value not in ('M', 'F'):
            raise ValueError('gender must be "M" or "F"')
        self._gender = value

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

    def time_worked(self):
        if self.leave_date:
            return self.leave_date - self.join_date
        else:
            return datetime.today() - self.join_date

    def __lt__(self, other):
        if not isinstance(other, Employee):
            raise TypeError(f'unsupported operation between types {type(self)} and {type(other)}')
        if self.time_worked() < other.time_worked():
            return True
        else:
            return False

    def __le__(self, other):
        if not isinstance(other, Employee):
            raise TypeError(f'unsupported operation between types {type(self)} and {type(other)}')
        if self.time_worked() <= other.time_worked():
            return True
        else:
            return False
        
    def __eq__(self, other):
        if not isinstance(other, Employee):
            raise TypeError('unsupported operation between types {type(self)} and {type(other)}')
        if self.time_worked() == other.time_worked():
            return True
        else:
            return False

    def __add__(self, *others):
        if self.leave_date:
                raise ValueError(f'{self} is not working in the company anymore.')
        for other in others:
            if not isinstance(other, Employee):
                raise TypeError('Unsupported operation between types {type(self)} and {type(other)}')
            if other is self:
                raise ValueError('Cannot team up the person to themselves.')
            if other.leave_date:
                raise ValueError(f'{other} is not working in the company anymore.')
        
        if (self, *others) in self.__class__.teams:
            print('The team already exists.')
        else:
            self.__class__.teams.append((self, *others))
