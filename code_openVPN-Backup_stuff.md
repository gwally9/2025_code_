1) mkdir -p /home/openvpnas/Backups/; chmod 0774 /home/openvpnas/Backups/

3) crontab -e
12 00 * * 0 /usr/local/bin/Backup_Database.sh

### for testing add: MM HH  * * * /usr/local/bin/Backup_Database.sh

4) create 
    vi /usr/local/bin/Backup_Database.sh; chmod 755 /usr/local/bin/Backup_Database.sh

#!/bin/bash
#
# Backup_Database.sh
# performs a snapshot of OpenVPN database resources
#
TARGET_DIR=/home/openvpnas/Backups
## create a snapshot of last weeks files
cd ${TARGET_DIR}
tar cvzf $(date +%m%d%Y)_SNAPSHOT.gz ./*.bak  2>archiving.log 1>&2
# create a weekly backup of the database
cd /usr/local/openvpn_as/etc/db
[ -e config.db ]&&sqlite3 config.db .dump>${TARGET_DIR}/config.db.bak
[ -e certs.db ]&&sqlite3 certs.db .dump>${TARGET_DIR}/certs.db.bak
[ -e userprop.db ]&&sqlite3 userprop.db .dump>${TARGET_DIR}/userprop.db.bak
[ -e log.db ]&&sqlite3 log.db .dump>${TARGET_DIR}/log.db.bak
[ -e config_local.db ]&&sqlite3 config_local.db .dump>${TARGET_DIR}/config_local.db.bak
[ -e cluster.db ]&&sqlite3 cluster.db .dump>${TARGET_DIR}/cluster.db.bak
[ -e notification.db ]&&sqlite3 notification.db .dump>${TARGET_DIR}/notification.db.bak 
cp -p ../as.conf ${TARGET_DIR}/as.conf.bak