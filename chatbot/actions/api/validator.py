class GeneralValidator:
    @staticmethod
    def is_valid_integer(value):
        try:
            value = int(value)
        except ValueError:
            return False
        return True
    @staticmethod
    def is_valid_float(value):
        try:
            value = float(value)
        except ValueError:
            return False
        return True
