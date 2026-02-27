# 💡 Docker Terms List

## 💠 Core Engine & Architecture

* **Docker Engine**
* **Docker Daemon (`dockerd`)**
* **Docker Client**
* **Docker Host**
* **Container**
* **Image**
* **Layer**
* **Registry**
* **Repository**
* **Tag**
* **Digest** (Content Addressable Identifier)
* **Manifest**
* **Manifest List** (Multi-arch images)

---

## 💠 The Build System (Dockerfile)

* **Dockerfile**
* **Base Image**
* **Build Context**
* **`.dockerignore`**
* **Multi-stage Build**
* **Instructions**

  * `FROM`
  * `RUN`
  * `CMD`
  * `LABEL`
  * `EXPOSE`
  * `ENV`
  * `ADD`
  * `COPY`
  * `ENTRYPOINT`
  * `VOLUME`
  * `USER`
  * `WORKDIR`
  * `ARG`
  * `ONBUILD`
  * `STOPSIGNAL`
  * `HEALTHCHECK`
  * `SHELL`
* **BuildKit**
* **Build Cache**
* **Squashing**

---

## 💠 Storage & Filesystems

* **Volume**
* **Bind Mount**
* **tmpfs Mount**
* **Named Volume**
* **Anonymous Volume**
* **Volume Driver**
* **Storage Driver**

  * Overlay2
  * aufs
  * devicemapper
  * btrfs
  * zfs
* **Copy-on-Write (CoW)**
* **Union File System (UnionFS)**
* **Writable Layer** (Container Layer)

---

## 💠 Networking

* **Bridge Network**
* **Host Network**
* **Overlay Network**
* **Macvlan Network**
* **None Network**
* **Network Driver**
* **Port Mapping / Publishing**
* **Exposed Ports**
* **DNS** (Embedded DNS)
* **IPAM** (IP Address Management)
* **Link** (Legacy)

---

## 💠 Orchestration & Tooling

* **Docker Compose**
* **Docker Swarm**
* **Swarm Mode**
* **Service**
* **Task**
* **Stack**
* **Node** (Manager / Worker)
* **Secret** (Docker Secrets)
* **Config** (Docker Configs)
* **Docker Desktop**
* **Docker Hub**
* **Docker Scan**

---

## 💠 Low-Level & Security

* **containerd**
* **runC**
* **CRI** (Container Runtime Interface)
* **OCI** (Open Container Initiative)
* **Namespaces**

  * PID
  * Net
  * IPC
  * Mnt
  * UTS
  * User
* **Control Groups (cgroups)**
* **Capabilities** (Linux Caps)
* **Seccomp Profiles**
* **AppArmor / SELinux**
* **Rootless Mode**
* **DIND** (Docker in Docker)
* **DOOD** (Docker out of Docker / Socket Binding)
* **Contexts** (Docker Context)
