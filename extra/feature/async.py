'''
  Threads, Processes vs Asynchronous
  Key Points:
  - Traditional Way for Parallel Programming with Threads
  - Processes is piese of CPU and memory that get allocates; Can have one or more Threads
  - Threads examples: Open multiple files, while waiting
  - Threads Problems:
    - Race Condition, since Memory Sharing and for unpredictable crashes
    - Harder to understand for source code that implement multiple threads
    - Overhead, while manage the threads, stop, restart, and take CPU time resources
  - The solution: Asynchoronous Programming. Examples: Futures & Promises. These are Functional Programming
'''

from dataclasses import dataclass
from typing import List, Protocol, Awaitable, Any, Union
from enum import Enum, auto
import string, random, asyncio


class MessageType(Enum):
  SWITCH_ON = auto(); SWITCH_OFF = auto(); CHANGE_COLOR = auto(); PLAY_SONG = auto()
  OPEN = auto(); CLOSE = auto(); FLUSH = auto(); CLEAN = auto()

@dataclass
class Message:
  device_id: str
  msg_type: MessageType
  data: str = ""


class HueLightDevice:
  async def connect(self) -> None:
    print("Connecting Hue Light.")
    
    # TODO: Here implementing some async dummy based of time interaction time limit
    await asyncio.sleep(0.5)
    print("Hue Light connected.")

  async def disconnect(self) -> None:
    print("Disconnecting Hue Light.")
    await asyncio.sleep(0.5)    
    print("Hue Light disconnected.")

  async def send_message(self, message_type: MessageType, data: str = "") -> None:
    print(f"Hue Light handling message of type {message_type.name} with data [{data}].")
    await asyncio.sleep(0.5)    
    print("Hue Light received message.")


class SmartSpeakerDevice:
  async def connect(self) -> None:
    print("Connecting to Smart Speaker.")
    await asyncio.sleep(0.5)
    print("Smart Speaker connected.")

  async def disconnect(self) -> None:
    print("Disconnecting Smart Speaker.")
    await asyncio.sleep(0.5)
    print("Smart Speaker disconnected.")

  async def send_message(self, message_type: MessageType, data: str = "") -> None:
    print(f"Smart Speaker handling message of type {message_type.name} with data [{data}].")
    await asyncio.sleep(0.5)
    print("Smart Speaker received message.")


class SmartToiletDevice:
  async def connect(self) -> None:
    print("Connecting to Smart Toilet.")
    await asyncio.sleep(0.5)
    print("Smart Toilet connected.")

  async def disconnect(self) -> None:
    print("Disconnecting Smart Toilet.")
    await asyncio.sleep(0.5)
    print("Smart Toilet disconnected.")

  async def send_message(self, message_type: MessageType, data: str = "") -> None:
    print(f"Smart Toilet handling message of type {message_type.name} with data [{data}].")
    await asyncio.sleep(0.5)
    print("Smart Toilet received message.")
    
def generate_id(length: int = 8):
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
  async def connect(self) -> None:
    ...

  async def disconnect(self) -> None:
    ...

  async def send_message(self, message_type: MessageType, data: str) -> None:
    ...


class IOTService:
  def __init__(self):
    self.devices: dict[str, Device] = {}

  async def register_device(self, device: Device) -> str:
    await device.connect()
    device_id = generate_id()
    self.devices[device_id] = device
    return device_id

  async def unregister_device(self, device_id: str) -> None:
    await self.devices[device_id].disconnect()
    del self.devices[device_id]

  def get_device(self, device_id: str) -> Device:
    return self.devices[device_id]

  async def run_program(self, program: Union[List[Message], Message]) -> None:
    
    # TODO: Prevent TypeError
    if isinstance(program, Message): program = [program]
    
    # TODO: Implement parallelism for each message conditions
    # * will help to iteration
    await asyncio.gather(*[self.send_msg(msg) for msg in program])

  async def send_msg(self, msg: Message) -> None:
    await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)


async def run_sequence(*functions: Awaitable[Any]) -> None:
  for function in functions: await function
  
async def run_parallel(*functions: Awaitable[Any]) -> None:
  await asyncio.gather(*functions)


async def main() -> None:
  service = IOTService()
  hue_light = HueLightDevice()
  speaker = SmartSpeakerDevice()
  toilet = SmartToiletDevice()
  
  # TODO: We implement parallelism, so must not wait registering one-by-one
  # The result will registring and connecting multiple device at the same time
  hue_light_id, speaker_id, toilet_id = await asyncio.gather(
    service.register_device(hue_light), 
    service.register_device(speaker),
    service.register_device(toilet)
  )

  # This two instances are doing program sequentially
  # so each of sub will executed one-by-one. So we need generic functions for running parallelism
  wake_up_program = [
    Message(hue_light_id, MessageType.SWITCH_ON),
    Message(speaker_id, MessageType.SWITCH_ON),
    Message(speaker_id, MessageType.PLAY_SONG, "Miles Davis - Kind of Blue"),
  ]

  await service.run_program(wake_up_program)
  
  # The firt 2 are doing in parallel, The last 2 are doing in sequential
  await run_parallel(
    service.run_program(Message(hue_light_id, MessageType.SWITCH_OFF)),
    service.run_program(Message(speaker_id, MessageType.SWITCH_OFF)),
    run_sequence(
      service.run_program(Message(toilet_id, MessageType.FLUSH)),
      service.run_program(Message(toilet_id, MessageType.CLEAN)),
    ),
    run_sequence(
      service.run_program(Message(speaker_id, MessageType.SWITCH_ON)),
      service.run_program(Message(speaker_id, MessageType.PLAY_SONG, "Miles Davis - Kind of Blue")),
    )
  )

if __name__ == '__main__':
  asyncio.run(main())