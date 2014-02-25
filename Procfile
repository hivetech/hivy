web: ./hivy/__main__.py --bind 0.0.0.0 --debug
serf: serf agent -node hivy -tag role=master -event-handler ./scripts/hivy-watchdog
# salt: salt-master -l debug -c /etc/salt
# minion: sudo salt-minion -l debug
