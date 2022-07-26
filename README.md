# EKS Observability with OpenSearch

This demonstration has the focus of provision Amazon EKS, Amazon Managed Prometheus, Amazon Managed Grafana and OpenSearch with Open Telemetry Collector in order to achive the complete observability stack. Logs, tracing and metrics.

## Steps

- Provision EKS Cluster with Managed NodeGroups X
- Setup ADOT Operator as Managed add-on in the cluster X
- Install metric-server, node-exporter and kube-state-metrics X
- Install OpenSearch using Helm
- Provision Amazon Managed Prometheus
- Provision Amazon Managed Grafana
- Setup Data Prepper in order to integrate with OpenSearch
- Create Open Telemetry Pipeline
- Deploy the sample applications inside the cluster
- Check OpenSearch Dashboard

## Provision EKS Cluster

```bash
eksctl create cluster -f observabilitydemo.yaml
```

Now wait about 15 minutes in order to have your cluster up and running.

Update your `kubeconfig`

```bash
aws eks update-kubeconfig --name eks-observablity-cluster --region us-east-2
```

## Setup ADOT Collector as Managed Add-On

> **Warning:** Your Amazon EKS cluster must be using Kubernetes version 1.19 or higher

Before installing the AWS Distro for OpenTelemetry (ADOT) add-on, you must meet the following prerequisites.

```bash
kubectl apply -f https://amazon-eks.s3.amazonaws.com/docs/addons-otel-permissions.yaml
```

### Installing cert-manager

The ADOT Operator uses admission webhooks to mutate and validate the Collector Custom Resource (CR) requests. In Kubernetes, the webhook requires a TLS certificate that the API server is configured to trust.

TBD: Change the cert-managed manifests to deploy it on infra nodes.

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.2/cert-manager.yaml
```

### Create ADOT IAM role

```bash
kubectl create ns monitoring

eksctl create iamserviceaccount \
    --name aws-otel-collector \
    --namespace monitoring \
    --cluster eks-observablity-cluster \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonPrometheusRemoteWriteAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
    --approve \
    --override-existing-serviceaccounts
```

### Install ADOT Operator Amazon EKS add-on

```bash
aws eks create-addon --addon-name adot --cluster-name eks-observablity-cluster
```

## Installing needed add-ons

### metric-server

Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. Metrics API can also be accessed by kubectl top, making it easier to debug autoscaling pipelines.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### kube-state-metrics

kube-state-metrics (KSM) is a simple service that listens to the Kubernetes API server and generates metrics about the state of the objects. (See examples in the Metrics section below.) It is not focused on the health of the individual Kubernetes components, but rather on the health of the various objects inside, such as deployments, nodes and pods.

```bash
kubectl apply -f ./add-ons/kube-state-metrics
```

### node-exporter

To get all the kubernetes node-level system metrics, you need to have a node-exporter running in all the kubernetes nodes. It collects all the Linux system metrics and exposes them via /metrics endpoint on port 9100

```bash
kubectl apply -f add-ons/kubernetes-node-exporter
```

## Install Opensearch Operator and Setup Cluster

**OpenSearch** is a community-driven, Apache 2.0-licensed open source search and analytics suite that makes it easy to ingest, search, visualize, and analyze data. Developers build with OpenSearch for use cases such as application search, log analytics, data observability, data ingestion, and more.

**The Kubernetes OpenSearch Operator** is used for automating the deployment, provisioning, management, and orchestration of OpenSearch clusters and OpenSearch dashboards.

Installing the operator.

```bash
cd ./add-ons/opensearch-operator/ && ./install.sh
```

Now that we have installed the operator, let's setup our OpenSearch Cluster.

```bash
kubectl apply -f opensearch-cluster.yaml
```

Now wait for the OpenSearch cluster to be up and running, if you want to follow the setup just execute the command below.

```bash
kubectl get pods -nmonitoring -w
```

## Provision AWS Managed Prometheus

Create AMP workspace

```bash
aws amp create-workspace --alias eks-observability-demo --region us-east-2
```

## Provision Managed Grafana

## Provision Data-Prepper

Data Prepper is a component of the OpenSearch project that accepts, filters, transforms, enriches, and routes data at scale.

```bash
cd ../ && kubectl apply -f ./data-prepper
```

## Creating ADOT Pipeline

Now that we have all the components up and running its time to create the OpenTelemetry Pipeline.

Getting Amazon Managed Prometheus `remote write` URL.

```bash
TBD
```

Change the URL inside the pipeline manifest.

```bash
TBD
```

Apply the pipeline manifest:

```bash
kubectl apply -f adot-collector/
```