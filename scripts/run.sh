#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# Supervisord 설정 파일에 uWSGI와 Streamlit 설정 추가
cat > /etc/supervisor/conf.d/app.conf << EOF
[program:uwsgi]
command=uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:streamlit]
command=streamlit run streamlit_apps/app1.py --server.port 8501 --server.address 0.0.0.0
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
EOF

# Supervisord 실행
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf