from django.shortcuts import render
from subprocess import run, PIPE
import sys

def runcode(request):
    if request.method == 'POST':
        script_path = '/Users/admin/Desktop/FSD/VoiceAssistant/assistant.py'
        
        try:
            out = run([sys.executable, script_path], shell=False, stdout=PIPE, bufsize=1, text=True)
            print(out.stdout)
        except Exception as e:
            print(f"Error running script: {e}")
            out = f"Error running script: {e}"

        return render(request, 'index.html', {'output': out.stdout})

    return render(request, 'index.html')
