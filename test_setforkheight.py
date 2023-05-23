from pyrobokit.agv_api import other

others_api = other.OtherAPI(ip="192.168.0.10")
forklift_height = other.ForkliftHeight(height = 0.1) # m
others_api.execute(forklift_height)
others_api.close()
