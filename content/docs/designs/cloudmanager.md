+++
title = 'Cloud Manager Design'
linkTitle = 'Cloud Manager'
date = 2024-09-27
draft = false
+++

**Author:** @hacktobeer <br>
**Published:** Sep 2024 <br>
**Document version:** 1.0 <br>
**Status:** Draft <br>

{{< callout type="info" >}}
**Request for comments**: If you have questions, comments or suggestions on this design, please share with the community and join the discussion.
<br>
**Discussion forum** for this design document can be found here: [https://github.com/orgs/openrelik/discussions/8](https://github.com/orgs/openrelik/discussions/8)
{{< /callout >}}

### Introduction

OpenRelik wants the capability to process cloud disks. This proposal describes a Cloud Manager service that handles all the cloud specific functionality and provides initial performance data. When dealing with cloud disks a lot of vendor specific tools need to be used to check, mount and unmount those disks. As OpenRelik strives to keep the workers as clean and dependency free as possible it makes sense to extract all of the cloud management functionality into a separate service.

The OpenRelik Cloud Manager is not limited to OpenRelik, it is a standalone component that can be used by any system that wishes to process cloud disks without having knowledge of the cloud specific dependencies.

### NBD

[Network Block Device (NBD)](https://en.wikipedia.org/wiki/Network_block_device) is a protocol that can be used to forward a block device from one machine to another machine. Using this technology one machine can handle the cloud disk management and the worker can access this disk over the NBD protocol as if it was a normal block device. The NBD protocol is supported natively in the linux kernel through the nbd kernel module. Both NBD server and client tools are [available](https://github.com/NetworkBlockDevice/nbd).

QEMU has a [NBD server tool](https://www.qemu.org/docs/master/tools/qemu-nbd.html) that is actively developed and used in QEMU and supports a variety of formats that can be exported as a block device. Supported formats are raw block device or dd, qcow, vmware, dmg and msft hyper-v images among [others](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-using_qemu_img-supported_qemu_img_formats#sect-Using_qemu_img-Supported_qemu_img_formats).

### Architecture

The proposed architecture of the Cloud Manager service.

* An API (FastApi) to mount, umount and query available cloud disks.
* An integrated server that exports block devices through the NBD protocol
* A container configuration so the CloudManager can run in a container.
* A python client library to easily mount/umount/query resources on the Cloud Manager service
* Integration into the OpenRelik Common Python library so Workers can call preprocess/postprocess functions on input without having to deal with mounting/unmounting of cloud disks.

### Workflow

A workflow demonstrating using a cloud disk between an OpenRelik Worker (*Worker*) and the OpenRelik CloudManager (*CM*) would work as follows:

1. *Worker* asks *CM* to make disk available (eg a GCE disk test) through an API call
2. *CM* uses cloud vendor tools to mount the disk as a block device on the *CM* machine
   * If the disk is already available it will lookup the disk to NBD port mapping.
3. *CM* provides *Worker* with a tcp port on which it can NBD mount the remote block device
4. *Worker* NBD mounts the remote block device locally as /dev/nbd0 using native linux nbd kernel support
5. *Worker* processes the disk as if it is a normal block device
6. When *Worker* is done it calls the unmount API on the *CM*
7. *CM* will check if the disk is used by any other *Worker* and unmount the disk using vendor cloud tools if it is not used anymore.

[![imagen](/cloudmanager.png)](/cloudmanager.png)

### Performance

As the cloud disk is mounted not directly on the OpenRelik Worker but mounted on the Cloud Manager and connected between them over the NBD protocol it is important to assess possible performance impact. Several tests have been conducted on GCP.

Conclusion: It seems the overhead of the NBD protocol is not limiting the read speed. The read speed seems to be only limited by the [GCE machine persistent disk limits](https://cloud.google.com/compute/docs/disks/performance#machine-type-disk-limits) per machine type. Advice would be to make the OpenRelik CloudManager a GCE machine type with lots of vCPUs and RAM to maximize disk read throughput.

### Test software
#### Gcloud
`gcloud compute instances attach-disk instance-test \--disk test-disk \--zone us-central1-b \--device-name=mydisk`

#### NBD server
`/usr/bin/qemu-nbd \--port=12345 \--shared=100 \-t \--pid-file=nbd.pid \-f raw /dev/disk/by-id/google-mydisk`

#### NBD client
`/sbin/nbd-client [nbd-server] 12345 /dev/nbd0`

#### Test\#1

Configuration:

* 2 GCE machines (e2-micro (2 vCPUs, 1 GB memory))
* GCE test-disk \-\> 10GB Debian buster balanced persistent disk

Test direct \-\> `dd | pv` directly on machine where GCE disk is attached

* dd on machine \-\> GCE disk
* $ sudo dd if=/dev/disk/by-id/google-test-disk|pv |dd of=/dev/null
* Average of 14.4 MB/sec

Test NBD \-\> `dd | pv` from machine where GCE disk is NBD attached through machine

* dd on nbd-client machine2 /dev/nbd0 \-\> NBD proto \-\>  machine2 \-\> GCE attached disk
* $ sudo dd if=/dev/nbd0|pv |dd of=/dev/null
* Average of 14.1 MB/sec

#### Test\#2
Configuration like Test\#1,but:

* 2 GCE machine (e2-standard-8 (8 vCPUs, 32 GB memory))
* GCE test-disk \-\> 200GB Debian buster balanced persistent disk

Test direct \-\> Average of 60.5 MB/sec
Test NBD \-\> Average of 58.9 MB/sec

#### Test\#2
Configuration like Test\#2,but:

* 3 parallel read tests on the same machine to simulate 3 worker instances that try to read from the same NBD disk

Test NBD \-\> All 3 reads stay consistent at 58.8 MB/sec \-\> seems like some nice NBD caching going on on the client side\!

#### Test\#3
Configuration like Test\#2,but:

* 2 parallel read tests on \*different\* machines to simulate 2 workers that try to read from the same NBD disk
* NBD server \-\> (e2-standard-8 (8 vCPUs, 32 GB memory))
* 2 NBD client machines \-\> (e2-standard-8 (8 vCPUs, 32 GB memory))

Test NBD machine 1 \-\> 58.8 MB/sec
Test NBD machine 2 \-\> 58.7 MB/sec

#### Test\#4
Configuration like Test\#2,but:

* 2 different machines that try to attach the same GCE disk and try to read from it directly

Test direct machine 1 \-\> 60MB/sec
Test direct machine 2 \-\> 60MB/sec

#### Test\#5
Configuration like Test\#4, but

* Not a cloud disk but a local disk image of 11GB of /dev/urandom data on the same machine as the NBD server
* 2 NBD client machines \-\> (e2-standard-8 (8 vCPUs, 32 GB memory))

Test NBD machine 1 \-\> 184MB/sec
Test NBD machine 2 \-\> 190MB/sec
