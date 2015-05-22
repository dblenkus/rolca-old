# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "rolcabox"
  config.vm.box_url = "http://data.domenblenkus.com/rolcabox.box"

  config.ssh.username = "domen"
  config.ssh.private_key_path = File.expand_path("~/.ssh/id_rsa")

  config.vm.network "forwarded_port", guest: 80, host: 1980
  config.vm.network "forwarded_port", guest: 8000, host: 1981

  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/webapps/rolcabox/rolca/", :owner => "rolcabox", :group => "webapps"

  config.vm.provider :virtualbox do |vb|
    vb.name = config.vm.box

    # Required for 64-bit guest OS
    vb.customize ["modifyvm", :id, "--ioapic", "on"]

    vb.customize ["modifyvm", :id, "--memory", "1024"]
    vb.customize ["modifyvm", :id, "--cpus", "1"]
  end

  config.vm.provision :shell, :path => "vagrant/provision.sh"

end
