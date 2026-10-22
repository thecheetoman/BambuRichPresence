import time
from discord_rpc import DiscordRPC

CLIENT_ID = "1561431854203142257"

rpc = DiscordRPC(CLIENT_ID)
rpc.connect()

rpc.update(
    details="Printing...",
    state="gah!"
)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    rpc.clear()
    rpc.disconnect()