class MootdxException(Exception):
    """Base notifier exception. Catch this to catch all of :mod:`notifiers` errors"""

    def __init__(self, *args, **kwargs):
        """
        Looks for ``provider``, ``message`` and ``data`` in kwargs
        :param args: Exception arguments
        :param kwargs: Exception kwargs
        """
        self.provider = kwargs.get('provider')
        self.response = kwargs.get('response')

        self.message = kwargs.get('message')
        self.data = kwargs.get('data')

        super().__init__(self.message)

    def __repr__(self):
        return f'<MOOTDXError: {self.message}>'


class MootdxValidationException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class MootdxModuleNotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class FileNeedRefresh(FileNotFoundError):
    pass
