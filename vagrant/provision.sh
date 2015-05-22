echo "Disabeling SELinux..."
setenforce 0

echo "Migrating database..."
cd /webapps/rolcabox/rolca
source ../bin/activate
python manage.py migrate >/dev/null 2>&1
