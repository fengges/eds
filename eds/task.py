
import time
from eds.service.task.taskservice import taskService
class Task:
    def statistics(self):
        print("start:"+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        taskService.statistics()
        taskService.updateLocation()


        print("end:"+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


task=Task()