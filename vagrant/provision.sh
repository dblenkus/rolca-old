cd /webapps/rolcabox/rolca
source ../bin/activate

echo "Updating requirements..."
yum install -y libffi-devel >/dev/null 2>&1
pip install requests[security] >/dev/null 2>&1
pip install -U pip >/dev/null 2>&1
pip install -Ur requirements.txt >/dev/null
pip install ipython >/dev/null

echo "Migrating database..."
python manage.py migrate --noinput >/dev/null

echo "Collecting static files..."
python manage.py collectstatic --noinput >/dev/null
chown -R rolcabox:webapps /webapps/rolcabox/static

echo "Creating superuser..."
DJANGO_USER_EMAIL='domen@blenkus.com' DJANGO_USER_PASSWORD='nm4xi6nb' python manage.py add_user --admin >/dev/null

echo "Disabeling firewall..."
systemctl stop firewalld
systemctl disable firewalld >/dev/null
