#    coding: UTF-8
#    User: haku
#    Date: 13-2-12
#    Time: 上午1:01
#
__author__ = 'haku'
from railgun import RailGun
import sys,urllib

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()
railgun.setTask(file("bing.yaml"));
railgun.setConfig("q", urllib.quote('帝国'))
railgun.fire();
nodes = railgun.getShells()
file = file("demo_bing.txt", "w+")
for id in nodes:
    node = nodes[id]
    file.write(node.get('title',[""])[0] + "\r\n")
    file.write(node.get('description',[""])[0] + "\r\n====================================\r\n")