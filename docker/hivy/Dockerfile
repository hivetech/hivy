# hivetech/intuition image
# A raring box with Intuition (https://github.com/hackliff/intuition installed
# and ready to use
# VERSION 0.1.0

# Administration
FROM quay.io/hackliff/node
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Speedup apt-get
RUN echo 'force-unsafe-io' | tee /etc/dpkg/dpkg.cfg.d/02apt-speedup
# Reduce image size
RUN echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache

# Dependencies
# FIXME blinker is temporary (fixed with the next push)
RUN apt-get install -y curl libssl-dev swig git-core python-pip python-dev python-setuptools && \
  pip install --use-mirrors --upgrade virtualenvwrapper blinker

# -------------------------------------------------------------- #
# ----    Hivy installation    --------------------------------- #
# -------------------------------------------------------------- #
#RUN pip install --use-mirrors hivy
RUN git clone https://github.com/hivetech/hivy.git --branch develop --depth 1 && \
  cd hivy && \
  python setup.py install

# Install Salt-master http://docs.saltstack.com/topics/installation/index.html
# copy hivy library states, and configure it
RUN apt-get -y install salt-master && \
  cp -r /hivy/genes/states /srv/salt && \
  cp -r /hivy/genes/data /srv/pillar && \
  sed -i 's/#auto_accept: False/auto_accept: True/g' /etc/salt/master

ENV NODE_ID hivy
ENV NODE_ROLE master
ADD ./startup-serf /usr/local/bin/startup-serf
ADD ./supervisor-hivy.conf /etc/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n"]

# Serf, ssh and hivy ports
EXPOSE 7946 7373 22 5000
