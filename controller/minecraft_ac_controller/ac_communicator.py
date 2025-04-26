import asyncio

from greeclimate.discovery import Discovery
from greeclimate.device import Device
import nest_asyncio 

class AirConditioner:
    def __init__(self):
        self.device = None

    async def _connect_device_background(self):
        discovery = Discovery()
        for device_info in await discovery.scan(wait_for=5):
            try:
                device = Device(device_info)
                await device.bind()
            except Exception as e:
                print(f"Unable to bind to gree device: {device_info}, error: {e}")
                continue

            self.device = device
            break

    def connect_device(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No loop is running -> we must manually create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Now loop is guaranteed to exist
        if loop.is_running():
            asyncio.create_task(self._connect_device_background())
        else:
            loop.run_until_complete(self._connect_device_background())

    async def _update_ac_background(self, temp=None, fan_speed=None):
        if temp is not None:
            self.device.target_temperature = temp
        if fan_speed is not None:
            self.device.fan_speed = fan_speed
        await self.device.push_state_update()

    def update_ac(self, temp=None, fan_speed=None):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # New task, but also wait for it
            task = asyncio.create_task(self._update_ac_background(temp, fan_speed))
            # Small trick to make sure it finishes even inside a running loop:
            nest_asyncio.apply()  # allows nested event loops
            loop.run_until_complete(task)
        else:
            loop.run_until_complete(self._update_ac_background(temp, fan_speed))
