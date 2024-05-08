# Virtual Machine Environment

### Setting up libvirt

`libvirt` is an open-source API, daemon and management tool for managing
platform virtualization. Install with:

``` {bash}
sudo apt install libvirt-clients libvirt-daemon-system libvirt0 libvirt-dev vagrant
```

### Environment Configuration

We need to add users in libvirt group:

``` {bash}
sudo usermod -aG libvirt <username>
```

#### Using a RAMdisk

A RAMdisk supports filesystem operations using RAM resources. It can
take the form of a hardware device or a virtual disk. If enough memory
is available, a RAMdisk will significantly speed up the creation and
destruction of virtual machines managed by Vagrant.

First step is to create and mount a RAMdisk:

``` {bash}
sudo mkdir /path/to/ramdisk
sudo mount -t tmpfs -o size=16G ramdisk0 /path/to/ramdisk
sudo chmod g+s /path/to/ramdisk
```

(We use `/media/ramdisk` on our Host.)

You may want to give group write access to the RAMdisk by creating and
managing a user group (on Debian, using the `libvirt` group works well).

We use 72GB RAMdisk on our server to support three developers without
issue. RAMdisks do not persist during reboots, so we cannot keep
permanent VMs in there.

It is possible to create the RAMdisk automatically on boot by adding the
following line to `/etc/fstab`:

```{fstab}
tmpfs /path/to/ramdisk tmpfs nodev,nosuid,noexec,nodiratime,size=72G 0 0
```

#### Configuring a libvirt Storage Pool

After creating the RAMdisk, we need to create a `libvirt` pool for each
user on it.  We create storage pools with a name given by
`vagrant_<username>` in the `/path/to/ramdisk/<username>` directory so
our scripts can more easily manage the pools.

Create a storage pool with the following:

``` {bash}
sudo virsh pool-define-as <vagrant_username> dir - - - - "/path/to/ramdisk/<username>"
sudo virsh pool-start <vagrant_username>
```

Create one pool per user to avoid VMs from different users trying to use
the same file name and leading do errors.  Add these lines to the
Vagrantfile, under the `libvirt` provider part.  Templates are kept
commented out in the provided file:


### Installing vagrant-libvirt
Vagrant plugin adds a Libvirt provider to Vagrant, allowing Vagrant
to control and provision machines via Libvirt toolkit.

``` {bash}
vagrant plugin install vagrant-libvirt
```
