#! /bin/bash


# const {
  NODE_ID="hivy"
  LOCAL_IP=$(hostname -I | cut -d" " -f1)
# }


docker run -d -name $NODE_ID \
  -e NODE_ROLE=master \
  -e NODE_ID=$NODE_ID \
  -e DOCKER_URL=http://$LOCAL_IP:4243 \
  -e SENTRY_DNS=$SENTRY_DNS \
  quay.io/hackliff/hivy
