from discord.ext.commands import Converter, BadArgument
from datetime import datetime


class InvalidBirthday(Exception):
    pass


class Birthday:
    @staticmethod
    def from_datetime(date: datetime):
        return Birthday(date.day, date.month)

    @staticmethod
    def from_string(argument: str):
        try:
            argument = argument.replace("'", "").replace('"', "")
            if "-" in argument:
                argument = argument.split("-")
            elif " " in argument:
                argument = argument.split(" ")
            if len(argument) != 2:
                raise BadArgument()
            try:
                day = int(argument[0])
            except ValueError:
                raise BadArgument("The day argument is invalid")
            try:
                month = int(argument[1])
            except ValueError:
                months = {
                    "january": "01",
                    "february": "02",
                    "march": "03",
                    "april": "04",
                    "may": "05",
                    "june": "06",
                    "july": "07",
                    "august": "08",
                    "september": "09",
                    "october": "10",
                    "november": "11",
                    "december": "12",
                }
                month = months.get(argument[1].lower(), None)
                if month is None:
                    raise BadArgument("The month argument is invalid")
            return Birthday(int(day), int(month))
        except InvalidBirthday:
            raise BadArgument("The Birthday is invalid.")

    def __init__(self, day: int, month: int):
        try:
            assert day <= 31
            assert month <= 12
        except AssertionError:
            raise InvalidBirthday()
        self.day = day
        self.month = month

    def __str__(self):
        day = str(self.day)
        month = str(self.month)
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month

        return f"{day}-{month}"

    def to_date(self, year: int):
        return datetime(year=year, month=self.month, day=self.day)


class BirthdayConverter(Converter):
    async def convert(self, ctx, argument: str):
        return Birthday.from_string(argument)
