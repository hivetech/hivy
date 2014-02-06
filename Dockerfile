# hivetech/intuition image
# A raring box with Intuition (https://github.com/hackliff/intuition installed
# and ready to use
# VERSION 0.1.0

# Administration
# hivetech/pyscience is an ubuntu 13.10 image with most popular python packages
FROM stackbrew/ubuntu:saucy
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Install telepathy ----------------------------
RUN git clone https://github.com/hivetech/hivy.git -b develop --depth 1 && \
  cd hivy && python setup.py install && \
  pip install honcho

CMD ["start", "-f", "/.hivy/Procfile"]
ENTRYPOINT ["honcho"]

EXPOSE 5000
