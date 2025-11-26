"""
Wrapper script to run the Streamlit app
This is needed for PyInstaller packaging
"""
import sys
import os
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the application directory
    os.chdir(application_path)
    
    # Set the main script path
    main_script = os.path.join(application_path, 'main.py')
    
    # Run streamlit
    sys.argv = ["streamlit", "run", main_script, "--server.headless=true"]
    sys.exit(stcli.main())
