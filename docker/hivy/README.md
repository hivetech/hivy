Unide Hivy
==========

[Unide](unide.co) platform controller and api frontend.

```console
docker run -d -name hivy \
  -e NODE_ROLE=controller \
  -e NODE_IMAGE=quay.io/hackliff/node \
  -e DOCKER_URL=172.17.0.3:4243 \
  -e SALT_MASTER_URL=172.17.0.3 \
  quay.io/hackliff/hivy
```
