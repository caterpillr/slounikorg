import subprocess
from datetime import datetime

while True:
    try:
        subprocess.run(['python3', 'main.py'])
    except Exception as e:
        print('! ! ! ! oopsie: ', str(e))
    print('### ### RESTART AT', datetime.now())

# help: https://m.habr.com/ru/post/350648/