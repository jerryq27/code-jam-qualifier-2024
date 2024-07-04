import sys
from enum import auto, StrEnum

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

    def __str__(self) -> str:
        return f'Quote {{ quote: {self.quote}, mode: {self.mode} }}'

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    # Parse the arguments and make sure the quote is one argument.
    arguments = []
    tokens = command.split()
    acceptable_quote_marks = ['"', '“']
    for i, token in enumerate(tokens):
        if token[0] in acceptable_quote_marks:
            quoted_token = ' '.join(tokens[i:])
            arguments.append(quoted_token)
            break
        else:
            arguments.append(token)
    # print(f'arguments: {arguments}')
    if(arguments[0].lower() != 'quote'):
        raise ValueError("Invalid command")
    
    # Valid quote command
    values_for_quote_class = ''
    second_argument = arguments[1].lower()
    if second_argument == 'list':
        print('do list command')
    elif second_argument[0] in acceptable_quote_marks:
        values_for_quote_class = (second_argument, VariantMode.NORMAL)
    else:
        # uwu and piglatin
        quote_value = arguments[2]
        uwu_piglatin_values = {
            'uwu': (quote_value, VariantMode.UWU),
            'piglatin': (quote_value, VariantMode.PIGLATIN),
        }
        values_for_quote_class = uwu_piglatin_values[second_argument]
    
    quote, mode = values_for_quote_class
    q = Quote(quote, mode)
    print(q)

# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)

if __name__ == '__main__':
    command = ''
    exit_commands = ['quit', 'q', 'exit']

    while command not in exit_commands:
        command = input('> ')
        if command in exit_commands:
            break

        run_command(command)
