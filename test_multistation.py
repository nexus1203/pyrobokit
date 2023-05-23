from pyrobotkit.agv_api import navigation

# perform a motion task to a multiple station

navi = navigation.NavigationAPI(ip = "192.168.0.10")
station1 = navigation.TaskOneStation(
                                      dest_id ="LM2", 
                                      source_id = "LM1,
                                      task_id = "action00001",
                                      max_speed = 0.8, #m/s
                                      method = "forward",
                                      duration = 0 # do not stop in between
                                    )
station2 = navigation.TaskOneStation(
                                      dest_id ="LM3", 
                                      source_id = "LM2,
                                      task_id = "action00002",  # must be non-identifical to other tasks
                                      max_speed = 0.8, #m/s
                                      method = "forward",
                                      duration = 0  # do not stop in between
                                    )
station3 = navigation.TaskOneStation(
                                      dest_id ="LM2", 
                                      source_id = "LM1,
                                      task_id = "action00003",  # must be non-identifical to other tasks
                                      max_speed = 0.8,  #m/s
                                      method = "forward",
                                      duration = 0  # do not stop in between
                                    )
# create a list of one station tasks
tasks = [station1, station2, station3]
multi_station = navigation.TaskMultiStation(tasks=tasks)

success = navi.execute(multi_station)
print(success)
# note all the methods are non waiting, so after the command is send the program will exit.
navi.close()
