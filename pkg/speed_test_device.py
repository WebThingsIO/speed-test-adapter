"""Speed test adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device, Property
import fastdotcom
import speedtest
import threading
import time


class SpeedTestSensor(Device):
    """Internet speed test device type."""

    def __init__(self, adapter, _id, provider, poll_interval, server_id):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        provider -- the data provider
        poll_interval -- interval at which to poll the provider, in minutes
        server_id -- ID of server to use (for speedtest.net)
        """
        Device.__init__(self, adapter, _id)
        self._type = ['MultiLevelSensor']
        self.type = 'multiLevelSensor'

        self.provider = provider
        self.poll_interval = poll_interval
        self.server_id = server_id

        self.name = 'Internet speed test'
        self.description = 'Internet speed test'

        self.properties['download'] = Property(
            self,
            'download',
            {
                '@type': 'LevelProperty',
                'title': 'Download Speed',
                'type': 'integer',
                'unit': 'Mbps',
                'minimum': 0,
                'maximum': 10000,  # 10 Tbps... had to have something here
                'readOnly': True,
            }
        )
        self.properties['download'].set_cached_value(0)

        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': 'https://{}'.format(self.provider),
            },
        ]

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        """Poll the device for changes."""
        while True:
            value = None

            if self.provider == 'fast.com':
                value = fastdotcom.fast_com()
            elif self.provider == 'speedtest.net':
                try:
                    t = speedtest.Speedtest()

                    if self.server_id is not None:
                        t.get_servers(servers=[self.server_id])
                    else:
                        t.get_servers()

                    t.get_best_server()
                    t.download()
                    value = t.results.download / 1000 / 1000
                except speedtest.SpeedtestException:
                    pass
            else:
                return

            if value is not None and value != 0:
                prop = self.properties['download']
                prop.set_cached_value(round(value))
                self.notify_property_changed(prop)

            time.sleep(self.poll_interval * 60)
