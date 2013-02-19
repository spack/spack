

class SpackException(Exception):
    def __init__(self, message):
        self.message = message


class FailedDownloadException(SpackException):
    def __init__(self, url):
        super(FailedDownloadException, self).__init__("Failed to fetch file from URL: " + url)
        self.url = url


class InvalidPackageNameException(SpackException):
    def __init__(self, name):
        super(InvalidPackageNameException, self).__init__("Invalid package name: " + name)
        self.name = name


class CommandFailedException(SpackException):
    def __init__(self, command):
        super(CommandFailedException, self).__init__("Failed to execute command: " + command)
        self.command = command
