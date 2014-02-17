#! /bin/bash

# main() {
  # Script owner informations
  echo "Event type: $SERF_EVENT"
  echo "Name: $SERF_SELF_NAME"
  echo "Role: $SERF_SELF_ROLE"
  echo "Tag Role (idem): $SERF_TAG_ROLE"
  echo "Tag Custom: $SERF_TAG_CUSTOM"

  # User event informations
  echo "User event type: $SERF_USER_EVENT"
  echo "User event ltime: $SERF_USER_LTIME"

  # Stdin informations
  while read line; do
    echo "Payload: ${line}"
    # standard handler sample: bar   127.0.0.1   lab   role=lab,service=database
    # custom handler: user event payload
    export instance_id=$(echo $line | awk '{print $1}')
    export VIRTUAL_IP=$(echo $line | awk '{print $2}')
    export ROLE=$(echo $line | awk '{print $3}')
    export TAGS=$(echo $line | awk '{print $4}')

    if [ "${ROLE}" != "lab" ]; then
      echo "${instance_id} is not a lab, ignoring member join."
      exit 0
    fi
  done
# }
