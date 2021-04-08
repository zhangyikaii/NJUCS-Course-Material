class SchemeError(Exception):
    def __repr__(self):
        return str(self)


class TerminatedError(SchemeError):
    def __init__(self):
        super().__init__("Error: program manually terminated")


class ParseError(SchemeError):
    pass


class SymbolLookupError(SchemeError):
    pass


class OperandDeduceError(SchemeError):
    pass


class TurtleDrawingError(SchemeError):
    pass


class CallableResolutionError(SchemeError):
    pass


class MathError(SchemeError):
    pass


class ComparisonError(SchemeError):
    pass


class TypeMismatchError(SchemeError):
    pass


class IrreversibleOperationError(SchemeError):
    pass


class FormatError(SchemeError):
    pass


class LoadError(SchemeError):
    pass


class OutOfMemoryError(SchemeError):
    pass
