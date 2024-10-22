import os 
import sys 
from django.core.management import execute_from_command_line 
 
def run_commands(): 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogApp.settings')    
 
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver': 
        print("Running command: runserver") 
        execute_from_command_line([sys.argv[0], 'runserver', '--noreload']) 
    if len(sys.argv) > 1 and sys.argv[1] == 'collectstatic': 
        print("Running command: collectstatic") 
        execute_from_command_line([sys.argv[0], 'collectstatic']) 
    else: 
        commands = ['makemigrations', 'migrate', 'createsuperuser'] 
         
        for command in commands: 
            print(f"Running command: {command}") 
            execute_from_command_line([sys.argv[0], command]) 
 
if __name__ == "__main__": 
    run_commands()

