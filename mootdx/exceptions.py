class MootdxException(Exception):
    """Base notifier exception. Catch this to catch all of :mod:`notifiers` errors"""

    def __init__(self, *args, **kwargs):
        """
        Looks for ``provider``, ``message`` and ``data`` in kwargs
        :param args: Exception arguments
        :param kwargs: Exception kwargs
        """
        self.provider = kwargs.get("provider")
        self.message = kwargs.get("message")

        self.data = kwargs.get("data")
        self.response = kwargs.get("response")

        super().__init__(self.message)

    def __repr__(self):
        return f"<MOOTDXError: {self.message}>"


class MootdxValidationException(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass
