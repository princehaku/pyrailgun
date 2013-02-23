# --encoding=utf-8
__author__ = 'haku'
from railgun import RailGun
import yaml

taskdata = yaml.load(file("res/testsite.yaml"))
railgun = RailGun()
railgun.settask(taskdata);
railgun.fire();
print railgun.getnodes('default')