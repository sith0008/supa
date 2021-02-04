# TODO: write script to start docker images, create volume and load data into DB if needed
#!/usr/bin/env bash
set -e

IMAGES_DIRECTORY='./images'

load_images()
{
  for image in "$1"/*.gz; do
    docker load < "$image"
  done
}

load_images $IMAGES_DIRECTORY