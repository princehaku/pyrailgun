#    coding: UTF-8
#    User: haku
#    Date: 13-2-12
#    Time: 1:01
#
__author__ = 'haku'
from pyrailgun import RailGun
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()

railgun.setTask(file("basic.json"))
railgun.fire();
nodes = railgun.getShells()
file = file("demo_basic.txt", "w+")
for id in nodes:
    node = nodes[id]
    file.write(node.get('score', [""])[0] + "\r\n")
    file.write(node.get('img', [""])[0] + "\r\n")
    file.write(node.get('description', [""])[0] + "\r\n====================================")