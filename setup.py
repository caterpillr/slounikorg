import subprocess, os
from datetime import datetime

os.system('NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program slounik')

while True:
    try:
        subprocess.run(['python3', 'main.py'])
    except Exception as e:
        print('! ! ! ! oopsie: ', str(e))
    print('### ### RESTART AT', datetime.now())

# help: https://m.habr.com/ru/post/350648/
