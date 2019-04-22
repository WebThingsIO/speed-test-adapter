"""Speed test adapter for Mozilla WebThings Gateway."""

from gateway_addon import Adapter, Database

from .speed_test_device import SpeedTestSensor


_TIMEOUT = 3


class SpeedTestAdapter(Adapter):
    """Adapter for internet speed test."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'speed-test-adapter',
                         'speed-test-adapter',
                         verbose=verbose)

        self.pairing = False
        self.provider = None
        self.poll_interval = None
        self.load_config()

    def load_config(self):
        """Load config from database and create device."""
        database = Database('speed-test-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        if not config or \
                'provider' not in config or \
                'pollInterval' not in config:
            return

        self.provider = config['provider']
        self.poll_interval = config['pollInterval']
        self.start_pairing()

    def start_pairing(self, timeout=None):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        _id = 'speed-test-sensor'
        if _id not in self.devices:
            device = SpeedTestSensor(
                self,
                _id,
                self.provider,
                self.poll_interval
            )
            self.handle_device_added(device)
