from pyrobotkit.agv_api import navigation

# perform a motion task to a single station

navi = navigation.NavigationAPI(ip = "192.168.0.10")
task = navigation.TaskOneStation(dest_id ="LM2", 
                                 max_speed = 0.8 #m/s
                                 method = "forward"
                                )
success = navi.execute(task)
print(success)
navi.close()
