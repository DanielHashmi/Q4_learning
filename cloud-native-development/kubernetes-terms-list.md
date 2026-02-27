# 💡 Kubernetes Terms List

---

## 💠 Infrastructure & Components
- **Cluster**
- **Node**
  - Control Plane (Master)
  - Worker
- **kube-apiserver**
- **etcd**
- **kube-scheduler**
- **kube-controller-manager**
- **cloud-controller-manager**
- **kubelet**
- **kube-proxy**
- **Container Runtime**
  - containerd
  - CRI-O
- **CRI** (Container Runtime Interface)

---

## 💠 Workload Resources
- **Pod**
- **Deployment**
- **ReplicaSet**
- **StatefulSet**
- **DaemonSet**
- **Job**
- **CronJob**
- **ReplicationController** *(Legacy, kept alive by nostalgia)*

---

## 💠 Networking
- **Service**
  - ClusterIP
  - NodePort
  - LoadBalancer
  - ExternalName
- **Ingress**
- **Ingress Controller**
- **Gateway API**
- **EndpointSlice**
- **NetworkPolicy**
- **CNI** (Container Network Interface)
- **CoreDNS**

---

## 💠 Storage
- **Volume**
- **PersistentVolume (PV)**
- **PersistentVolumeClaim (PVC)**
- **StorageClass**
- **CSI** (Container Storage Interface)
- **Ephemeral Volume**

---

## 💠 Configuration & Security
- **ConfigMap**
- **Secret**
- **Namespace**
- **RBAC**
  - Role
  - ClusterRole
  - RoleBinding
  - ClusterRoleBinding
- **ServiceAccount**
- **Admission Controllers**
  - Mutating
  - Validating
- **Pod Security Standards / Admission**
- **NetworkPolicy**

---

## 💠 Scheduling & Management
- **Labels & Selectors**
- **Annotations**
- **Taints & Tolerations**
- **Affinity & Anti-affinity**
  - Node
  - Pod
- **PriorityClass & Preemption**
- **Resource Requests & Limits**
- **LimitRange**
- **ResourceQuota**
- **Horizontal Pod Autoscaler (HPA)**
- **Vertical Pod Autoscaler (VPA)**
- **Pod Disruption Budget (PDB)**

---

## 💠 Advanced Concepts & Metadata
- **Custom Resource Definition (CRD)**
- **Operator Pattern**
- **Finalizer**
- **Owner References**
- **Garbage Collection**
- **Sidecar Containers**
- **Init Containers**
- **Ephemeral Container**
- **Control Groups (cgroups)**
- **Lease**

---

## 💠 Tooling
- **kubectl**
- **Helm**
- **Kustomize**
- **kubeadm**
- **Minikube**
