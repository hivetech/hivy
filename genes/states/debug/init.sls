---
{% for file, ext in pillar.get('date_files', {}).items() %}
# cmd.run
date > /tmp/{{ file }}.{{ ext }}:
  cmd:
    - run
{% endfor %}

https://github.com/{{ pillar['repository'] }}:
  git.latest:
    - rev: develop
    - target: {{ pillar['destination'] }}
