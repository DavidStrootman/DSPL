from dspl.helper import PrintableBase


class TestPrintableBase:
    def test_print(self):
        base = PrintableBase()
        assert str(base) == "PrintableBase"

    def test_repr(self):
        base = PrintableBase()
        base.base = base
        assert repr(base) == "PrintableBase: {'base': PrintableBase: {...}}"
