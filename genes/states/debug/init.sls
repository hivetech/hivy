---
{% for file, ext in pillar.get('date_files', {}).items() %}
# cmd.run
date > /tmp/{{ file }}.{{ ext }}:
  cmd:
    - run
{% endfor %}
