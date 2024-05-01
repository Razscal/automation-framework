class SystemException(Exception):
    """
        The exception happens during initialization and get transaction data
    """
    def __init__(self, *args):
        super().__init__(*args)
    
    @staticmethod
    def raise_exception(exception: Exception) -> None:
        # Send email or perform other advanced exception handling
        print(exception)

class BusinessException(Exception):
    """
        The exception happens when facing any errors during automation
    """
    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def raise_exception(exception: Exception) -> None:
        # Send email or perform other advanced exception handling
        print(exception)