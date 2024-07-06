import warnings
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

        if self.mode != VariantMode.NORMAL:
            self.quote = self._create_variant()

        if len(self.quote) > MAX_QUOTE_LENGTH:
            raise ValueError('Quote is too long')

    def __str__(self) -> str:
        return f'Quote {{ quote: {self.quote}, mode: {self.mode} }}'

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        quote = self.quote

        if self.mode == VariantMode.UWU:
            return self._uwuify(quote)
        elif self.mode == VariantMode.PIGLATIN:
            return self._piglatinify(quote)
        else:
            raise ValueError(f'Invalid mode: {self.mode}')

    def _uwuify(self, quote):
        # Take care of the easier requirements first
        for lowercase_char in ['l', 'r']:
            quote = quote.replace(lowercase_char, 'w')
        for uppercase_char in ['L', 'R']:
            quote = quote.replace(uppercase_char, 'W')

        # Need offset for index since quote length changes when added U-U/u-u replacement.
        u_u_offset = 0
        for i, character in enumerate(quote):
            if character in ['u', 'U']:
                # String slicing op
                modified_quote = quote[:i+u_u_offset] + f'{character}-{character}' + quote[i+1+u_u_offset:]
                if len(modified_quote) > MAX_QUOTE_LENGTH:
                    warnings.warn('Quote too long, only partially transformed')
                    break
                else:
                    u_u_offset += 2
                    quote = modified_quote
        if quote == self.quote:
            raise ValueError('Quote was not modified')
        return quote

    def _piglatinify(self, quote):
        quote_mark = quote[0]
        quoteless_quote = quote[1:-1]

        words = quoteless_quote.split()

        vowels = ['a', 'e', 'i', 'o', 'u']
        punctuation_marks = (',', '.', '!', '?')

        piglatin_words = []
        for word in words:
            punctuation_mark = ''
            has_punctuation_mark = word.endswith(punctuation_marks)
            if has_punctuation_mark:
                punctuation_mark = word[-1]
                word = word[:-1]
            
            # First vowels, much simpler
            if word[0] in vowels:
                piglatin_word = f'{word}way'
                if has_punctuation_mark:
                    piglatin_word += punctuation_mark
                
                piglatin_words.append(piglatin_word)
            else:
                # Cursed double for loop, but need to iterate the characters
                for i, character in enumerate(word):
                    if character in vowels:
                        # I love string slicing in Python
                        consonant_cluster = word[:i]
                        piglatin_word = word[i:] + f'{consonant_cluster}ay'
                        if has_punctuation_mark:
                            piglatin_word += punctuation_mark
                        
                        piglatin_words.append(piglatin_word)
                        break

        no_words_changed = len(piglatin_words) == 0
        not_all_words_changed = len(words) > len(piglatin_words)
        
        if no_words_changed or not_all_words_changed:
            raise ValueError('Quote was not modified')

        # Everything checks out!
        piglatin_words[0] = piglatin_words[0].lower().title()
        quote = quote_mark + ' '.join(piglatin_words) + quote_mark
        return quote

def parse_command_into_arguments(command: str) -> list[str]:
    # Parse the arguments and make sure the quote sentence is one argument.
    arguments = []
    tokens = command.split()
    for i, token in enumerate(tokens):
        if token[0] in ['"', '“']:
            quoted_token = ' '.join(tokens[i:])
            # Check if anyone tried to be cheeky and pass additional arguments after the quote
            if quoted_token[-1] not in ['"', '“']:
                raise ValueError('Invalid additional arguments')
            arguments.append(quoted_token)
            break
        else:
            arguments.append(token)
    return arguments

def determine_variant(arguments: list[str]) -> tuple[str, VariantMode]:
    second_arg = arguments[1]

    if second_arg[0] in ['"', '“']:
        return (second_arg, VariantMode.NORMAL)
    elif second_arg.lower() == 'uwu':
        return (arguments[2], VariantMode.UWU)
    elif second_arg.lower() == 'piglatin':
        return (arguments[2], VariantMode.PIGLATIN)
    else:
        raise ValueError('Invalid command')

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
    arguments = parse_command_into_arguments(command)
    if arguments[0].lower() != 'quote' :
        raise ValueError('Invalid command')
    elif len(arguments) == 1 :
        raise ValueError('No additional arguments specified')
    
    # Valid quote command
    second_argument = arguments[1].lower()
    if second_argument == 'list':
        quotes = Database.get_quotes()
        for quote in quotes:
            print(quote)
    else:
        quote, mode = determine_variant(arguments)
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
