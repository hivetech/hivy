# hivetech/intuition image
# A raring box with Intuition (https://github.com/hackliff/intuition installed
# and ready to use
# VERSION 0.1.0

# Administration
# hivetech/pyscience is an ubuntu 13.10 image with most popular python packages
FROM stackbrew/ubuntu:saucy
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Speedup apt-get
RUN echo 'force-unsafe-io' | tee /etc/dpkg/dpkg.cfg.d/02apt-speedup
# Reduce image size
RUN echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache

# Enable the necessary sources and upgrade to latest
RUN echo "deb http://archive.ubuntu.com/ubuntu saucy main universe multiverse restricted" > /etc/apt/sources.list && \
  apt-get -y update && apt-get upgrade -y -o DPkg::Options::=--force-confold

# Local settings
RUN apt-get install -y language-pack-fr wget git-core python-pip python-dev


# Install telepathy ----------------------------
RUN pip install --use-mirrors hivy

CMD ["--bind", "0.0.0.0", "--debug"]
ENTRYPOINT ["hivy"]

EXPOSE 5000
