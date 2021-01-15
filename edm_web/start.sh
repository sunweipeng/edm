time=$(date "+%Y-%m-%d")
nohup python3 manage.py runserver -h 127.0.0.1 -p 8090 > logs/nohup_manage_${time}.out 2>&1 &