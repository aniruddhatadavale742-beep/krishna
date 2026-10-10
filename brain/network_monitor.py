import socket


class NetworkMonitor:
    """
    Checks whether KRISHNA has internet access.
    """

    def is_internet_available(self):

        try:
            socket.create_connection(
                ("1.1.1.1", 53),
                timeout=3
            )

            return True

        except OSError:
            return False