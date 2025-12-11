# Definitions

## pods
- smallest deployable units of computing that you can create and manage in K8s
- min 1 container
- shared components
  - shared storage
  - shared networking
  - specific instructions on how to run
  - context
    - what you are interacting with
    - what user & namespace

## cluster
- set of nodes
- managed by k8s control plane

## Deployments
- objext that allows you to easily replicate an application via pods
  - describe desired state
  - deployment controller changes the actual state at a controlled rate
- bluprint for running applicatioins in a cluster
- high level instruction manual for control plane
- defines
  - container image to use
  - desired state
  - detailed config specs
  - scaling requirements

## services
- method to expose your applications running on one or more pods in a cluster
  - expose is at net infra level
- help close inter-cluster communications gap
- expose groups of pods as a logical endpoint
  - ex. frontend, backend, db
- enables decoupling of microservices via abstraction

## kubeconfig
- file which organizes information about clusters, users, namespaces and auth mechanisms
- used with `kubectl` tool for coms with k8s API
- context
  - element used to group access parameters under one name
  - yaml

## namespace
- way to logically group together resources that are related

## manifest file
- has custom config for creating a cluster
- includes AWS resources to be deployed including
  - vpc
  - availability zones
  - cloudwatch
  - fargate profiles
  - IAM

# IAM 
## EKS
- service user
- service admin
  - full access
## k8s / 'kubectl'
- AWS IAM Principal
  - role or user
  - can assign k8s permissions
  - can assign IAM permissions for AWS resources
- User in openid connect
  - OIDC provider
  - Assign k8s permissions
  - cannot assign IAM permissions for AWS resources
## default
- AWS IAM authenticator installed with in cluster control plane
- allow IAM principals access via
  - access entry
    - requires k8s 1.23
    - includes exactly one IAM Principal ARN
    - each entry contains a type
      - ex. ec2 linux, ec2 windows, fargate_linux, standard
    - cannot change after access entry creation
    - recommended method
  - AWS auth config map
    - depricating
    

# command tools
## `kubectl` interacts with k8s
- health checks
- deployments
- scaling
  - replicas
  - compute
- retrieving logs
  - view logs
### useful commands
```bash
kubectl get all
```

## `eksctl` interacts with amazon eks
- create and manage clusters
- delete and update clusters
- setting up and managing node groups
- setup integration with other AWS services
  - vpcs
- uses cloudformation on the back end

### useful commands
```bash
eksctl create cluster -f [manifest.yaml]
```

# Heirarchy
## Organized by Type
nodes are physical, namespaces are logical
```
Cluster
│
├── Control Plane
│   ├── API Server
│   ├── etcd
│   ├── Controller Manager
│   └── Scheduler
│
├── Nodes
│   ├── Node 1
│   │   ├── Pod 1
│   │   │   ├── Container 1
│   │   │   └── Container 2
│   │   ├── Pod 2
│   │   │   └── Container 1
│   │   └── ...
│   ├── Node 2
│   │   ├── Pod 1
│   │   │   └── Container 1
│   │   └── ...
│   └── ...
│
├── Namespaces
│   ├── Namespace 1
│   │   ├── Pod 1
│   │   ├── Service 1
│   │   ├── Deployment 1
│   │   │   └── ReplicaSet 1
│   │   │       └── Pod 1
│   │   ├── StatefulSet 1
│   │   ├── DaemonSet 1
│   │   ├── Job 1
│   │   ├── CronJob 1
│   │   ├── ConfigMap 1
│   │   ├── Secret 1
│   │   ├── PersistentVolume 1
│   │   ├── PersistentVolumeClaim 1
│   │   └── Ingress 1
│   ├── Namespace 2
│   │   └── ...
│   └── ...
│
└── NetworkPolicies
    ├── Policy 1
    └── Policy 2
```
## Namespaces
Namespaces do not have a direct one-to-one mapping with nodes. Instead, namespaces are a logical separation within the cluster, and pods within a namespace can be scheduled on any node in the cluster.
```
Cluster
│
├── Control Plane
│   ├── API Server
│   ├── etcd
│   ├── Controller Manager
│   └── Scheduler
│
├── Nodes
│   ├── Node 1
│   │   ├── Pod (Namespace 1)
│   │   ├── Pod (Namespace 2)
│   │   └── ...
│   ├── Node 2
│   │   ├── Pod (Namespace 1)
│   │   ├── Pod (Namespace 3)
│   │   └── ...
│   └── ...
│
├── Namespaces
│   ├── Namespace 1
│   │   ├── Pod 1 (Node 1)
│   │   ├── Pod 2 (Node 2)
│   │   └── ...
│   ├── Namespace 2
│   │   ├── Pod 1 (Node 1)
│   │   └── ...
│   └── ...
│
└── NetworkPolicies
    ├── Policy 1
    └── Policy 2
```
