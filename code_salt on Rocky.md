Installing Salt Server on Rocky

To install a Salt server in Rocky Linux, you first need to ensure that your system packages are up-to-date and install Python 3, as SaltStack is based on Python. After updating your system, you should install the SaltStack repository to download the latest version of SaltStack

Next, import the GPG key for the SaltStack repository and add the repository to your system For Rocky Linux, you can use the following commands:

```bash
sudo rpm --import https://repo.saltproject.io/salt/py3/redhat/9/x86_64/SALT-PROJECT-GPG-PUBKEY-2023.pub
curl -fsSL https://repo.saltproject.io/salt/py3/redhat/9/x86_64/latest.repo | sudo tee /etc/yum.repos.d/salt.repo
```

After setting up the repository, you can install the SaltStack Master package using the following command:

```bash
sudo dnf install salt-master
```

You will need to configure the SaltStack Master by editing the `/etc/salt/master` file. Uncomment the `interface:` option and change the IP address to your master server's IP address

Finally, enable and start the `salt-master` service:

```bash
sudo systemctl enable salt-master && sudo systemctl start salt-master
```

To install and configure SaltStack Minions, follow similar steps on each minion server. Install the `salt-minion` package, configure the minion to connect to the master server's IP address or hostname in the `/etc/salt/minion` file, and start the `salt-minion` service

