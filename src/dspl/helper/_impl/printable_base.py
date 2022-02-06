class PrintableBase:
    """Printable Baseclass."""

    def __str__(self) -> str:
        """
        Used to get the name of the class.
        :return: The type of this object
        """
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        """
        The formatted dictionary representation of this object.
        :return: A formatted string representation of the __dict__ property of this object.
        """
        return f"{str(self)}: {self.__dict__}"
