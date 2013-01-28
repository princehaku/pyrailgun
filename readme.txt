How To Use?

test.yaml

action: main
name: "vc¶¯Âþ"
subaction:
- action: fetcher
  url: http://www.verycd.com/base/cartoon/page
  subaction:
  - action: parser
    rule: .entry_cover_list li
    subaction:
    - action: node
      group: default
      subaction:
        - {action: parser, rule: '.entry_cover .cover_img', setField: img}
        - {action: parser, strip: 'true', rule: '.entry_cover .score', setField: score}
        - {action: parser, rule: '.bio a', setField: dest}
        - action: fetcher
          url: http://s.taobao.com/${#dest}
          subaction:
          - {action: parser, rule: '#title', setField: description}

then in your script

import yaml

taskdata = yaml.load(file("res/testsite.yaml"))
railgun = RailGun()
railgun.settask(taskdata);
railgun.fire();
print railgun.getnodes()
