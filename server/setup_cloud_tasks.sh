#!/bin/bash

set -ex

gcloud beta tasks queues create-app-engine-queue gumo-default-queue --project=gumo-example
