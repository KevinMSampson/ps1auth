# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
export AD_URL="ldap://localhost"
export AD_DOMAIN="VAGRANT"
export AD_BASEDN="CN=Users,DC=vagrant,DC=lan"
export AD_BINDDN="Administrator@VAGRANT"
export AD_BINDDN_PASSWORD="aeng3Oog"
export SECRET_KEY="deesohshoayie6PiGoGaghi6thiecaingai2quab2aoheequ8vahsu1phu8ahJio"
export ZOHO_AUTHTOKEN="add-your-auth-token"
export PAYPAL_RECEIVER_EMAIL="money@vagrant.lan"

# update the system
sudo apt-get update
#sudo apt-get -y upgrade

#install dependencies
sudo apt-get -y install build-essential python-dev postgresql git postgresql-server-dev-all libldap2-dev libsasl2-dev python-pip libacl1-dev

#build samba
wget -c 'http://ftp.samba.org/pub/samba/samba-latest.tar.gz'
tar -xvzf samba-latest.tar.gz
cd samba-*
./configure
make
sudo make install

#download startup script
sudo wget -O /etc/init/samba-ad-dc.conf 'http://anonscm.debian.org/gitweb/?p=pkg-samba/samba.git;a=blob_plain;f=debian/samba-ad-dc.upstart;hb=HEAD'
# patch startup script
sudo sed -i 's|exec samba -D|exec /usr/local/samba/sbin/samba -D|g' /etc/init/samba-ad-dc.conf
sudo /usr/local/samba/bin/samba-tool domain provision --realm=vagrant.lan --domain=${AD_DOMAIN} --server-role=dc --use-rfc2307 --adminpass=${AD_BINDDN_PASSWORD}
sudo service samba-ad-dc start
cd ..

#install python packages
sudo pip install -r /vagrant/requirements/local.txt

# environment variables
echo "export AD_URL=${AD_URL}" >> .bashrc
echo "export AD_DOMAIN=${AD_DOMAIN}" >> .bashrc
echo "export AD_BASEDN=${AD_BASEDN}" >> .bashrc
echo "export AD_BINDDN=${AD_BINDDN}" >> .bashrc
echo "export AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}" >> .bashrc
echo "export SECRET_KEY=${SECRET_KEY}" >> .bashrc
echo "export ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}" >> .bashrc
echo "export PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}" >> .bashrc

#setup database
sudo -u postgres createuser --superuser vagrant
sudo -u vagrant createdb ps1auth
sudo -u vagrant -E /usr/bin/python /vagrant/manage.py syncdb
sudo -u vagrant -E /usr/bin/python /vagrant/manage.py migrate

#setup database

#supervisor
sudo apt-get install -y supervisor
echo "[program:ps1auth]" > /etc/supervisor/conf.d/ps1auth.conf
echo "command = /usr/bin/python /vagrant/manage.py runserver 0.0.0.0:8000" >> /etc/supervisor/conf.d/ps1auth.conf
echo "user = vagrant" >> /etc/supervisor/conf.d/ps1auth.conf
echo "redirect_stderr = true" >> /etc/supervisor/conf.d/ps1auth.conf
echo "stdout_logfile=/vagrant/vagrant.log" >> /etc/supervisor/conf.d/ps1auth.log
echo "environment=AD_URL='${AD_URL}',AD_BASEDN='${AD_BASEDN}',AD_BINDDN='${AD_BINDDN}',AD_BINDDN_PASSWORD='${AD_BINDDN_PASSWORD}',SECRET_KEY='${SECRET_KEY}',ZOHO_AUTHTOKEN='${ZOHO_AUTHTOKEN}',PAYPAL_RECEIVER_EMAIL='${PAYPAL_RECEIVER_EMAIL}',AD_DOMAIN='${AD_DOMAIN}'" >> /etc/supervisor/conf.d/ps1auth.conf
sudo supervisorctl reread
sudo supervisorctl update
SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 8000, host: 8000,
      auto_correct: true
end
