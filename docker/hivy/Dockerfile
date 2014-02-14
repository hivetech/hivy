# hivetech/intuition image
# A raring box with Intuition (https://github.com/hackliff/intuition installed
# and ready to use
# VERSION 0.1.0

# Administration
# hivetech/pyscience is an ubuntu 13.10 image with most popular python packages
FROM quay.io/hackliff/node
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Speedup apt-get
RUN echo 'force-unsafe-io' | tee /etc/dpkg/dpkg.cfg.d/02apt-speedup
# Reduce image size
RUN echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache

# Dependencies
RUN apt-get install -y libssl-dev swig git-core python-pip python-dev python-setuptools && \
  pip install --use-mirrors --upgrade virtualenvwrapper

# -------------------------------------------------------------- #
# ----    Hivy installation    --------------------------------- #
# -------------------------------------------------------------- #
#RUN pip install --use-mirrors hivy
RUN git clone --branch develop --depth 1 https://github.com/hivetech/hivy.git && \
  cd hivy && \
  python setup.py install

ENV NODE_ID hivy
ADD ./supervisor-hivy.conf /etc/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n"]

# Serf, ssh and hivy ports
EXPOSE 7946 7373 22 5000
