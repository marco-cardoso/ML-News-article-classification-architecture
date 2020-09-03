class ContentNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoModelFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
