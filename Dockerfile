# hivetech/hivy image
# Hive controller https://github.com/hivetech/hivy
# VERSION 0.0.1

# Administration
FROM hivetech/base

# Install Hivy
ADD . /hivy
RUN /hivy/build/hivy.sh
RUN mkdir /etc/service/hivy && \
  mv /hivy/build/startup-hivy /etc/service/hivy/run

# TODO Install ansible

# Override consul behavior to act as server
RUN mv /hivy/build/startup-consul /etc/service/consul/run

# Override salt-minion to become salt-master
RUN /hivy/build/salt-master.sh
RUN mkdir /etc/service/salt-master && \
  rm -r /etc/service/salt-minion && \
  mv /hivy/build/startup-salt-master /etc/service/salt-master/run

# Clean up APT when done.
RUN /build/cleanup.sh

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# Expose serf, ssh / ansible and hivy ports
EXPOSE 7946 7373 22 5000
