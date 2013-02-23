# --encoding=utf-8
__author__ = 'haku'
from railgun import RailGun
import json

taskdata = json.load(file("res/testsite.json"))
railgun = RailGun()
railgun.settask(taskdata);
railgun.fire();
print railgun.getnodes('default')