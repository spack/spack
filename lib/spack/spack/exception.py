

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


class VersionParseException(SpackException):
    def __init__(self, msg, spec):
        super(VersionParseException, self).__init__(msg)
        self.spec = spec


class UndetectableVersionException(VersionParseException):
    def __init__(self, spec):
        super(UndetectableVersionException, self).__init__("Couldn't detect version in: " + spec, spec)


class UndetectableNameException(VersionParseException):
    def __init__(self, spec):
        super(UndetectableNameException, self).__init__("Couldn't parse package name in: " + spec)
