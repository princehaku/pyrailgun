#    coding: UTF-8
#    User: haku
#    Date: 13-2-12
#    Time: 上午1:01
#
__author__ = 'haku'
from railgun import RailGun
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()
railgun.settask(file("res/testsite.yaml"));
railgun.fire();
nodes = railgun.getnodes()
file = file("tmp/result.txt", "w+")
for id in nodes:
    node = nodes[id]
    if (node.get('score') != None and len(node.get('score')) > 0):
        file.write(node.get('score')[0] + "\r\n")
    file.write(node.get('img')[0] + "\r\n")