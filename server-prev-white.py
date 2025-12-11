import os
import subprocess
import sys
import re
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

def check_and_install_markdown():
    try:
        import markdown
    except ImportError:
        print("Markdown package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        import markdown
    
    try:
        import pymdownx
    except ImportError:
        print("pymdown-extensions package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymdown-extensions"])
        import pymdownx

def render_markdown_file(file_path):
    """
    Render the markdown file to HTML with:
    - footnotes support
    - code highlighting
    - sane lists
    - basic tables
    Also:
    - convert '~~strike~~' to <del> tags before rendering
    - after rendering, convert list items that start with [ ] / [x] to checkboxes
    """
    import markdown

    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert 2-space or 3-space indented list items to 4-space for proper nesting
    # This handles both ordered and unordered lists
    lines = md_content.split('\n')
    processed_lines = []
    for line in lines:
        # Check if line starts with 2 or 3 spaces followed by a list marker
        if re.match(r'^  [-*+\d]', line) or re.match(r'^   [-*+\d]', line):
            # Count leading spaces
            spaces = len(line) - len(line.lstrip())
            # Convert to 4-space indentation
            line = '    ' + line.lstrip()
        processed_lines.append(line)
    md_content = '\n'.join(processed_lines)

    # Simple strikethrough support: convert '~~text~~' -> <del>text</del>
    # Do this before markdown so the <del> is preserved as HTML.
    md_content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', md_content, flags=re.DOTALL)
    
    # Highlight support: convert '==text==' -> <mark>text</mark>
    md_content = re.sub(r'==(.*?)==', r'<mark>\1</mark>', md_content, flags=re.DOTALL)

    # Render markdown with extensions that improve list handling and footnotes
    from pymdownx import emoji
    
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'extra',         # collection of useful extensions
            'footnotes',     # footnotes support
            'fenced_code',
            'codehilite',
            'tables',
            'nl2br',         # converts newlines to <br> tags
            'pymdownx.emoji',  # emoji support
        ],
        extension_configs={
            'pymdownx.emoji': {
                'emoji_index': emoji.twemoji,
                'emoji_generator': emoji.to_svg,
            }
        }
    )

    # Post-process rendered HTML to convert task list markers into checkboxes.
    # Matches <li>[ ] text</li> or <li>[x] text</li> (with possible leading whitespace/newlines).
    # Use DOTALL so multiline list items are handled.
    html_content = re.sub(
        r'<li>\s*\[\s\]\s*(.*?)</li>',
        r'<li><input type="checkbox"> <span>\1</span></li>',
        html_content,
        flags=re.DOTALL,
    )
    html_content = re.sub(
        r'<li>\s*\[\s*[xX]\s*\]\s*(.*?)</li>',
        r'<li><input type="checkbox" checked> <span>\1</span></li>',
        html_content,
        flags=re.DOTALL,
    )

    return html_content

class MarkdownHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Debug: log incoming request line and client address
        try:
            client = f"{self.client_address[0]}:{self.client_address[1]}"
        except Exception:
            client = str(self.client_address)
        print(f"Request: {self.command} {self.path} from {client}")

        if self.path == "/":
            # Dynamically generate the index page with buttons
            markdown_files = [f for f in os.listdir('.') if f.endswith('.md')]
            file_buttons = ''.join(
                f'<button onclick="location.href=\'{f}\'">{f}</button>'
                for f in markdown_files
            )
            html_response = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Markdown Files</title>
                <style>
                    body {{
                        font-family: sans-serif;
                        padding: 1em;
                        max-width: 1200px;
                        margin: auto;
                    }}
                    .button-container {{
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.5em;
                    }}
                    button {{
                        padding: 0.5em 1em;
                        font-size: 1em;
                        cursor: pointer;
                        background-color: #8585ad;
                        color: white;
                        border: none;
                        border-radius: 5px;
                    }}
                    button:hover {{
                        background-color: #666699;
                    }}
                    #output {{
                        margin-top: 1em;
                    }}
                    input[type="checkbox"] {{
                        margin-right: 0.5em;
                    }}
                    code {{
                        background-color: #f4f4f4;
                        border-radius: 3px;
                        font-family: monospace;
                        padding: 0.15em 0.3em;
                    }}
                    pre {{
                        background-color: #f4f4f4;
                        color: black;
                        border-radius: 5px;
                        overflow-x: auto;
                        padding: 0.8em;
                    }}
                    .codehilite {{
                        background-color: #f4f4f4;
                        color: black;
                        padding: 1em;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                    del {{
                        color: #444;
                    }}
                    span.task-text {{
                        transition: background-color 0.2s ease;
                    }}
                    input[type="checkbox"]:checked + span.task-text {{
                        text-decoration: line-through;
                        background-color: #e8e8e8;
                    }}
                </style>
                <script>
                document.addEventListener("DOMContentLoaded", () => {{
                    // Make checkboxes interactive and preserve visual state
                    document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {{
                        checkbox.addEventListener("change", () => {{
                            const span = checkbox.nextElementSibling;
                            if (checkbox.checked) {{
                                span.style.textDecoration = "line-through";
                                span.style.backgroundColor = "#e8e8e8";
                            }} else {{
                                span.style.textDecoration = "none";
                                span.style.backgroundColor = "transparent";
                            }}
                        }});
                    }});
                }});
                </script>
            </head>
            <body>
                <h1>Markdown Files</h1>
                <div class="button-container">
                    {file_buttons}
                </div>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path.endswith(".md"):
            # remove leading '/'
            raw = self.path[1:]
            # decode percent-encoding
            file_path = unquote(raw)
            # normalize to avoid confusion about cwd
            abs_path = os.path.abspath(file_path)
            exists = os.path.exists(abs_path)
            print(f"Resolved path: '{file_path}' -> '{abs_path}', exists={exists}")
            if exists and abs_path.startswith(os.path.abspath('.')):
                html_content = render_markdown_file(abs_path)
                html_response = self.render_page(html_content, file_path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_response.encode('utf-8'))
                return
            else:
                # more verbose 404 for debugging
                msg = f"File Not Found: requested={file_path} resolved={abs_path} exists={exists}"
                print(msg)
                self.send_error(404, msg)
                return

        return super().do_GET()

    def render_page(self, html_content, file_name):
        # Dynamically generate the buttons for all Markdown files
        markdown_files = [f for f in os.listdir('.') if f.endswith('.md')]
        file_buttons = ''.join(
            f'<button onclick="location.href=\'{f}\'">{f}</button>'
            for f in markdown_files
        )

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{file_name} - Markdown Viewer</title>
            <style>
                body {{
                    font-family: sans-serif;
                    padding: 1em;
                    max-width: 1200px;
                    margin: auto;
                }}
                .button-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5em;
                    margin-bottom: 1em;
                }}
                button {{
                    padding: 0.5em 1em;
                    font-size: 1em;
                    cursor: pointer;
                    background-color: #8585ad;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }}
                button:hover {{
                    background-color: #666699;
                }}
                #output {{
                    margin-top: 1em;
                }}
                ul, ol {{
                    margin: 1em 0;
                    padding-left: 2em;
                }}
                ul {{
                    list-style-type: disc;
                }}
                ol {{
                    list-style-type: decimal;
                }}
                li {{
                    margin: 0.5em 0;
                }}
                ul ul, ol ul {{
                    list-style-type: circle;
                    margin-top: 0.25em;
                }}
                ol ol, ul ol {{
                    list-style-type: lower-alpha;
                    margin-top: 0.25em;
                }}
                input[type="checkbox"] {{
                    margin-right: 0.5em;
                }}
                code {{
                    background-color: #f4f4f4;
                    border-radius: 3px;
                    font-family: monospace;
                    padding: 0.15em 0.3em;
                }}
                pre {{
                    background-color: #f4f4f4;
                    color: black;
                    border-radius: 5px;
                    overflow-x: auto;
                    padding: 0.8em;
                }}
                .codehilite {{
                    background-color: #f4f4f4;
                    color: black;
                    padding: 1em;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                del {{
                    color: #444;
                }}
                mark {{
                    background-color: #ffff00;
                    padding: 0.1em 0.2em;
                }}
                .twemoji {{
                    height: 1.2em;
                    width: 1.2em;
                    vertical-align: text-bottom;
                }}
                table {{
                    border-collapse: collapse;
                    margin: 1em 0;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 0.75em;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                span.task-text {{
                    transition: background-color 0.2s ease;
                }}
                input[type="checkbox"]:checked + span.task-text {{
                    text-decoration: line-through;
                    background-color: #e8e8e8;
                }}
            </style>
            <script>
                document.addEventListener("DOMContentLoaded", () => {{
                    document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {{
                        checkbox.addEventListener("change", () => {{
                            const span = checkbox.nextElementSibling;
                            if (checkbox.checked) {{
                                span.style.textDecoration = "line-through";
                                span.style.backgroundColor = "#e8e8e8";
                            }} else {{
                                span.style.textDecoration = "none";
                                span.style.backgroundColor = "transparent";
                            }}
                        }});
                    }});
                }});
            </script>
        </head>
        <body>
            <h1>Markdown Viewer</h1>
            <div class="button-container">
                {file_buttons}
            </div>
            <h2>{file_name}</h2>
            <div id="output">{html_content}</div>
        </body>
        </html>
        """

def start_server():
    port = 8000
    print(f"Starting server on http://localhost:{port}")
    httpd = HTTPServer(("0.0.0.0", port), MarkdownHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    check_and_install_markdown()
    start_server()
