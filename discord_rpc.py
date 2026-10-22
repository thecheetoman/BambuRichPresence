import time
from pypresence import Presence


class DiscordRPC:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.rpc = None
        self.connected = False
        self.start_time = int(time.time())

    def connect(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            print("sucesfuly conected")
        except Exception as e:
            self.connected = False
            print("failed to connect, error: " + e)

    def disconnect(self):
        if self.rpc:
            try:
                self.rpc.close()
            except Exception:
                pass

        self.connected = False
        print("disconnected")

    def clear(self):
        if not self.connected:
            return

        try:
            self.rpc.clear()
        except Exception as e:
            print("could not clear status, error: " + e)

    def update(
        self,
        details: str,
        state: str = "",
        large_image: str = "solidworks_logo",
        large_text: str = "SOLIDWORKS",
        small_image: str | None = None,
        small_text: str | None = None,
    ):
        if not self.connected:
            return

        payload = {
            "details": details,
            "state": state,
            "start": self.start_time,
            "large_image": large_image,
            "large_text": large_text,
        }

        if small_image:
            payload["small_image"] = small_image

        if small_text:
            payload["small_text"] = small_text

        try:
            self.rpc.update(**payload)
        except Exception as e:
            print("failed to update!" + e)