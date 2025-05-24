import os
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

def check_and_install_markdown():
    try:
        import markdown
    except ImportError:
        print("Markdown package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        import markdown

def preprocess_task_lists(md_content):
    import re

    # Skip code blocks by splitting the content into non-code and code sections
    def replace_task_lists(match):
        content = match.group(0)
        # Replace '- [ ]' with unchecked checkboxes and wrap text in a <span>
        content = re.sub(r'^- \[ \](.*)', r'<input type="checkbox"><span>\1</span>', content, flags=re.MULTILINE)
        # Replace '- [x]' with checked checkboxes and wrap text in a <span>
        content = re.sub(r'^- \[x\](.*)', r'<input type="checkbox" checked><span>\1</span>', content, flags=re.MULTILINE)
        return content

    # Regex to match code blocks
    code_block_pattern = r'(```.*?```|`.*?`)'

    # Process only non-code sections
    processed_content = re.sub(
        code_block_pattern,
        lambda match: match.group(0),  # Leave code blocks unchanged
        md_content
    )
    # Apply task list replacements to non-code sections
    processed_content = re.sub(r'^(?!```)(- \[.\].*)', replace_task_lists, processed_content, flags=re.MULTILINE)
    return processed_content

def render_markdown_file(file_path):
    import markdown
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        # Preprocess task lists to convert them into HTML checkboxes
        md_content = preprocess_task_lists(md_content)
        # Render the Markdown content into HTML with the 'nl2br' extension
        html_content = markdown.markdown(md_content, extensions=['toc', 'fenced_code', 'codehilite', 'tables', 'nl2br'])
    return html_content

class MarkdownHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Dynamically generate the index page with buttons
            markdown_files = [f for f in os.listdir('.') if f.endswith('.md')]
            file_buttons = ''.join(f'<button onclick="location.href=\'/{f}\'">{f}</button>' for f in markdown_files)
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
                        background-color: #f4f4f4; /* Light gray background for inline code */
                        border-radius: 3px;
                        font-family: monospace;
                    }}
                    pre {{
                        background-color: #f4f4f4; /* Light gray background for code blocks */
                        color: black; /* text color */
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                    .codehilite {{
                        background-color: #f4f4f4; /* Light gray background for highlighted code */
                        color: black; /* text color */
                        padding: 1em;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                </style>
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
            file_path = unquote(self.path[1:])
            if os.path.exists(file_path):
                html_content = render_markdown_file(file_path)
                html_response = self.render_page(html_content, file_path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_response.encode('utf-8'))
                return
            else:
                self.send_error(404, "File Not Found")
                return
        return super().do_GET()

    def render_page(self, html_content, file_name):
        # Dynamically generate the buttons for all Markdown files
        markdown_files = [f for f in os.listdir('.') if f.endswith('.md')]
        file_buttons = ''.join(f'<button onclick="location.href=\'/{f}\'">{f}</button>' for f in markdown_files)
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
                input[type="checkbox"] {{
                    margin-right: 0.5em;
                }}
                code {{
                    background-color: #f4f4f4; /* Light gray background for inline code */
                    border-radius: 3px;
                    font-family: monospace;
                }}
                pre {{
                    background-color: #f4f4f4; /* Light gray background for inline code */
                    color: black; /* text color */
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                .codehilite {{
                    background-color: #f4f4f4; /* Light gray background for inline code */
                    color: black; /* text color */
                    padding: 1em;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
            <script>
                document.addEventListener("DOMContentLoaded", () => {{
                    document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {{
                        checkbox.addEventListener("change", () => {{
                            const span = checkbox.nextElementSibling; // Get the <span> next to the checkbox
                            if (checkbox.checked) {{
                                span.style.textDecoration = "line-through";
                            }} else {{
                                span.style.textDecoration = "none";
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