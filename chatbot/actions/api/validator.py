class GeneralValidator:
    @staticmethod
    def is_valid_integer(self, value):
        try:
            value = int(value)
        except ValueError:
            return False
        return True
    @staticmethod
    def is_valid_float(self, value):
        try:
            value = float(value)
        except ValueError:
            return False
        return True
