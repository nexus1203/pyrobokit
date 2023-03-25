from seer_robokit.tcp_transport import TcpTransport
from seer_robokit.tcp_transport import API_PORT_CTRL
import time

ip_address = "192.168.x.x"
motion_req = 2010

transport = TcpTransport(ip_address, API_PORT_CTRL)
print(transport.connected)

# read velocity
data = transport.send_n_receive(1, 1005, {})
vx = data["vx"]
vy = data["vy"]
w = data["w"]
print(f"speed now:: vx={vx}, vy={vy}, w={w}")

# set velocity to 50% of current velocity
set_vx = 0.5 * vx
set_vy = 0.5 * vy
set_w = 0.5 * w

data = transport.send_n_receive(1, motion_req, {
    "vx": set_vx,
    "vy": set_vy,
    "w": set_w
})
print("speed set:: ", data)
time.sleep(0.25)

# continue to decrease velocity by 10% every 0.5 seconds for 2 seconds
# then return to original velocity
for i in range(4):
    data = transport.send_n_receive(1, 1005, {})
    now_vx = data["vx"]
    now_vy = data["vy"]
    now_w = data["w"]
    print(f"speed now:: vx={now_vx}, vy={now_vy}, w={now_w}")
    time.sleep(0.25)

    set_vx = 0.9 * now_vx
    set_vy = 0.9 * now_vy
    set_w = 0.9 * now_w
    data = transport.send_n_receive(1, motion_req, {
        "vx": set_vx,
        "vy": set_vy,
        "w": set_w
    })
    print("speed set:: ", data)
    time.sleep(0.25)

# set velocity back to original velocity
data = transport.send_n_receive(1, motion_req, {"vx": vx, "vy": vy, "w": w})
print("speed set:: ", data)
time.sleep(0.25)
data = transport.send_n_receive(1, 1005, {})
print(f"speed now:: vx={data['vx']}, vy={data['vy']}, w={data['w']}")
print("done")
