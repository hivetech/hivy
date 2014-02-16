# hivetech/node image
# Base node for unide (unide.co)
# VERSION 0.0.1
# docker run -d -name node -e SALT_MASTER=192.168.0.11 -h node hackliff/node

# Administration
FROM saltstack/ubuntu-13.10-minimal
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Speedup apt-get
RUN echo 'force-unsafe-io' | tee /etc/dpkg/dpkg.cfg.d/02apt-speedup
# Reduce image size
RUN echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache

# Upgrade System and install global dependencies
RUN apt-get update && \
  apt-get upgrade -y -o DPkg::Options::=--force-confold && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  openssh-server language-pack-fr wget build-essential git-core supervisor unzip


# -------------------------------------------------------------- #
# ----    Salt-minion installation    -------------------------- #
# -------------------------------------------------------------- #
RUN apt-get install -y salt-minion


# -------------------------------------------------------------- #
# ----    SSH Preparation    ----------------------------------- #
# -------------------------------------------------------------- #
# FIXME SSH Issue. It managed to make it work but not sure about side effects
# See http://stackoverflow.com/questions/18173889/cannot-access-centos-sshd-on-docker
RUN echo 'root:unide' | chpasswd && \
  test -d /var/run/sshd || mkdir /var/run/sshd && \
  sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \
  sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config


# -------------------------------------------------------------- #
# ----    Serf installation    --------------------------------- #
# -------------------------------------------------------------- #
ADD https://dl.bintray.com/mitchellh/serf/0.4.1_linux_amd64.zip serf.zip
RUN unzip serf.zip && \
  rm serf.zip && \
  mv serf /usr/local/bin/


# -------------------------------------------------------------- #
# ----    Startup scripts    ----------------------------------- #
# -------------------------------------------------------------- #
ADD ./startup-serf /usr/local/bin/startup-serf
ADD ./startup-salt-minion /usr/local/bin/startup-salt-minion
ADD ./supervisor-node.conf /etc/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n"]

# Expose serf, and ssh / ansible ports
# NOTE salt-minion: maybe 4510, 4511
EXPOSE 7946 7373 22
