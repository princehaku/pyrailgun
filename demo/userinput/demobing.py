#    coding: UTF-8
#    User: haku
#    Date: 13-2-12
#    Time: 1:01
#
__author__ = 'haku'
from pyrailgun import RailGun
import sys, urllib

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()
railgun.setTask(file("bing.json"));
query = raw_input("Please Input Query\r\n")
railgun.setGlobalData("q", urllib.quote(query))
railgun.fire();
nodes = railgun.getShells()
file = file("demo_bing.txt", "w+")
for id in nodes:
    node = nodes[id]
    print "entry  " + node.get('title',[""])[0]
    file.write(node.get('title',[""])[0] + "\r\n")
    file.write(node.get('description',[""])[0] + "\r\n====================================\r\n")