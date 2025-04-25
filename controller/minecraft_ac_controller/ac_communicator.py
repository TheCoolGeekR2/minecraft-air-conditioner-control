import asyncio

from greeclimate.discovery import Discovery, Listener
from greeclimate.device import Device, DeviceInfo


class AirConditioner:
    def __init__(self):
        pass

    async def _connect_device_background(self):
        discovery = Discovery()
        for device_info in await discovery.scan(wait_for=5):
            try:
                device = Device(device_info)
                await device.bind()  # Device will auto bind on update if you omit this step
            except CannotConnect:
                _LOGGER.error("Unable to bind to gree device: %s", device_info)
                continue

        self.device = device

    def connect_device(self):
        asyncio.run(self._connect_device_background())

    def update_ac(self, temp=None, fan_speed=None):
        if temp:
            self.device.target_temperature = temp
        if fan_speed:
            self.device.fan_speed = fan_speed

        asyncio.run(self.device.push_state_update())
