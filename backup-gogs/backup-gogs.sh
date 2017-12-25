#!/bin/bash
# 指定dropbox_uploader.sh脚本的保存目录
SCRIPT_DIR="/root/backup"
# 上传到DropBox的文件夹
DROPBOX_DIR="/backup/$(date +"%Y.%m.%d")"
# 需要保存的服务器文件夹，可以用空格隔开多个文件夹
BACKUP_SRC="/home/git/gogs-repositories"
# 服务器上临时的备份保存文件夹
LOCAL_BAK_DIR="/root/backup"
# MySQL相应配置
MYSQL_SERVER="localhost"
MYSQL_USER="root"
MYSQL_PASS="1325xlg"
# 数据备份压缩后的文件名称
DBBakName=Data_$(date +"%Y%m%d").tar.gz
WebBakName=Web_$(date +"%Y%m%d").tar.gz
# 已过期备份数据的名称（3天前的数据会被删除）
Old_DROPBOX_DIR="/backup/$(date -d -3day +"%Y.%m.%d")"
OldDBBakName=Data_$(date -d -3day +"%Y%m%d").tar.gz
OldWebBakName=Web_$(date -d -3day +"%Y%m%d").tar.gz

# 导出MySQL数据库备份（所有数据库），并压缩为指定文件名
mysqldump -u $MYSQL_USER -h $MYSQL_SERVER -p$MYSQL_PASS --events --all-databases > $LOCAL_BAK_DIR/Database.sql
tar zcvf $LOCAL_BAK_DIR/$DBBakName $LOCAL_BAK_DIR/Database.sql
rm -rf $LOCAL_BAK_DIR/Database.sql
# 压缩需要保存的文件夹为指定文件名
tar zcvf $LOCAL_BAK_DIR/$WebBakName $BACKUP_SRC

# 上传压缩后的备份文件到指定的DropBox目录
$SCRIPT_DIR/dropbox_uploader.sh upload $LOCAL_BAK_DIR/$DBBakName $DROPBOX_DIR/$DBBakName
$SCRIPT_DIR/dropbox_uploader.sh upload $LOCAL_BAK_DIR/$WebBakName $DROPBOX_DIR/$WebBakName
echo -e "upload done!"

# 上传完成后删除服务器上及DropBox中已经过期的备份数据，节省空间
rm -rf $LOCAL_BAK_DIR/$OldDBBakName $LOCAL_BAK_DIR/$OldWebBakName
$SCRIPT_DIR/dropbox_uploader.sh delete $Old_DROPBOX_DIR/
echo -e "delete old backup done"