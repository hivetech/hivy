web: hivy --bind 0.0.0.0 --debug
serf: serf agent -node hivy -tag role=master -event-handler hivy-watchdog
# salt: salt-master -l debug -c /etc/salt
