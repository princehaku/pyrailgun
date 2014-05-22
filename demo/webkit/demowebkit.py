#    coding: UTF-8
#    User: haku
#    Date: 13-2-12
#    Time: 上午1:01
#
__author__ = 'haku'
from pyrailgun import RailGun
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()
railgun.setTask(file("webkit.json"));
railgun.fire();
nodes = railgun.getShells()
file = file("demo_webkit.txt", "w+")
for id in nodes:
    node = nodes[id]
    file.write(node.get('content',[""])[0] + "\r\n====================================")