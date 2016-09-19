# Overview

This interface layer handles the communication with SDN providers like flannel via the `sdn-plugin` interface.

# Usage

## Requires

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected` The relation is established, but the sdn
    may not yet have provided any connection or service information.

  * `{relation_name}.available` the SDN provider has provided its
    configuration information.
    The provided information can be accessed via the following methods:
      * `sdn-plugin.get_configuration()`



For example, a common application for this is configuring an applications
SDN configuration, like Kubernetes.

```python
@when('sdn-plugin.available', 'docker.available')
def container_sdn_setup(sdn):
    sdn_config = sdn.get_configuration()

    with open('/etc/default/docker', 'w') as stream:
      stream.write('DOCKER_OPTS=bip={0},mtu={1]}'.format(sdn_config['subnet'], sdn_config['mtu']))

```


## Provides

A charm providing this interface is plugging into its related principal charm.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected` One or more clients of any type have
    been related. The charm should call the following methods to provide the
    appropriate information to the clients:

    * `{relation_name}.set_configuration(mtu=mtu, subnet=subnet, cidr=cidr)`

Example:

> Note, this example will use the Flannel subnet.env file, which has a format like follows:

```shell
FLANNEL_NETWORK=10.1.0.0/16
FLANNEL_SUBNET=10.1.8.1/24
FLANNEL_MTU=1410
FLANNEL_IPMASQ=false
```

And the consuming python code:

```python
@when('flannel.sdn.configured', 'sdn-plugin.connected')
def relay_sdn_configuration(host):

  config = hookenv.config()

  with open('/var/run/flannel/subnet.env') as f:
      flannel_config = f.readlines()

  for f in flannel_config:
      if "FLANNEL_SUBNET" in f:
          value = f.split('=')[-1].strip()
          subnet = value
      if "FLANNEL_MTU" in f:
          value = f.split('=')[1].strip()
          mtu = value

    host.send_sdn_info(mtu, subnet, hookenv.config('cidr'))
```


# Contact Information

### Maintainer
- Charles Butler <charles.butler@canonical.com>


# Etcd

- [Flannel](https://coreos.com/flannel/docs/latest/) home page
- [Flannel bug trackers](https://github.com/coreos/flannel/issues)
- [Flannel Juju Charm](http://jujucharms.com/?text=flannel)
