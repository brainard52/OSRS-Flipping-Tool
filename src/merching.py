#!/usr/bin/env python3 -c "exit()"

# import appdirs
import webview

html = """
[$HTML$]
"""

if __name__ == '__main__':
    window = webview.create_window("Landon's Merching Tool", url='merching.html')
    webview.start(debug=True)
