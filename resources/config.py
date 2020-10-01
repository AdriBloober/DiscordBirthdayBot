from os import environ

EMPTY_ATTRIBUTE = "#12412419"


class EnvironmentMustBeSet(Exception):
    def __init__(self, environment_name):
        super().__init__(environment_name)


class Config:

    # Database configuration
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USER = EMPTY_ATTRIBUTE
    DB_PASSWORD = EMPTY_ATTRIBUTE
    DB_DB = EMPTY_ATTRIBUTE

    BOT_TOKEN = EMPTY_ATTRIBUTE
    BOT_PREFIX = "Bi!"

    ADMIN_WEBHOOK_URL = ""

    INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=705817352411021322&permissions=92224&scope=bot"
    GITHUB_LINK = "https://github.com/AdriBloober/DiscordBirthdayBot"


config = Config()

ignore_attributes = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
]

not_set_environments = []
for attribute in dir(config):
    if not attribute in ignore_attributes and attribute.upper() == attribute:
        replacement = environ.get(attribute, None)
        if not replacement in [None, EMPTY_ATTRIBUTE]:
            setattr(config, attribute, replacement)
        elif getattr(config, attribute) is EMPTY_ATTRIBUTE:
            not_set_environments.append(attribute)
if len(not_set_environments) > 0:
    environments = (
        str(not_set_environments).replace("[", "").replace("]", "").replace("'", "")
    )
    raise EnvironmentMustBeSet(f"The environment() {environments} aren't/isn't set.")

print("Config was successfully loaded")
