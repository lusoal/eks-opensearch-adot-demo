#!/bin/bash

helm repo add opensearch-operator https://opster.github.io/opensearch-k8s-operator/
helm repo update

helm install opensearch-operator opensearch-operator/opensearch-operator -f values.yaml -n monitoring