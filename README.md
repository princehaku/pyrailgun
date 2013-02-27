How To Use?

testsite.yaml

```
action: main
name: "vc动漫"
subaction:
- action: fetcher
  url: http://www.verycd.com/base/cartoon/page${1,1}${0,9}
  subaction:
  - action: parser
    rule: .entry_cover_list li
    subaction:
    - action: shell
      group: default
      subaction:
        - {action: parser, rule: '.entry_cover .cover_img', setField: img}
        - {action: parser, rule: 'a', pos: 0, attr: href, setField: src}
        - {action: parser, strip: 'true', rule: '.entry_cover .score', setField: score}
        - {action: parser, rule: '.bio a', setField: dest}
        - action: fetcher
          url: http://www.verycd.com${#src}
          subaction:
          - {action: parser,strip: 'true', rule: '#contents_more', setField: description}
```

then in your script

```
from railgun import RailGun

railgun = RailGun()
railgun.setTask(file("testsite.yaml"));
railgun.fire();
nodes = railgun.getShells('default')
print nodes
```

then you can get all the nodes in a list
[{img:xxx,src:xxx,score:xxx,dest:xxx,description:xxx},{img:xxx,src:xxx,score:xxx,dest:xxx,description:xxx}]

怎么使用?
首先你需要创建一个对应站点的规则文件
比如testsite.yaml

```
action: main
name: "vc动漫"
subaction:
- action: fetcher
  url: http://www.verycd.com/base/cartoon/page${1,1}${0,9}
  subaction:
  - action: parser
    rule: .entry_cover_list li
    subaction:
    - action: shell
      group: default
      subaction:
        - {action: parser, rule: '.entry_cover .cover_img', setField: img}
        - {action: parser, rule: 'a', pos: 0, attr: href, setField: src}
        - {action: parser, strip: 'true', rule: '.entry_cover .score', setField: score}
        - {action: parser, rule: '.bio a', setField: dest}
        - action: fetcher
          url: http://www.verycd.com${#src}
          subaction:
          - {action: parser,strip: 'true', rule: '#contents_more', setField: description}
```

然后在代码里面把它作为一个任务加入到railgun

```
from railgun import RailGun

railgun = RailGun()
railgun.setTask(file("testsite.yaml"));
railgun.fire();
nodes = railgun.getShells('default')
print nodes
```

然后你就可以得到一个包含了所有解析后数据的节点列表
[{img:xxx,src:xxx,score:xxx,dest:xxx,description:xxx},{img:xxx,src:xxx,score:xxx,dest:xxx,description:xxx}]