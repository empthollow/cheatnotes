import os
import subprocess
import sys
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote


def check_and_install_markdown():
    """Ensure required markdown packages are installed."""
    try:
        import markdown  # noqa: F401
    except ImportError:
        print("Markdown package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        import markdown  # noqa: F401

    try:
        import pymdownx  # noqa: F401
    except ImportError:
        print("pymdown-extensions package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymdown-extensions"])
        import pymdownx  # noqa: F401


def render_markdown_file(file_path: str) -> str:
    """Render a markdown file into HTML with extra features."""
    import markdown
    from pymdownx import emoji

    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert 2-space or 3-space indented list items to 4-space for proper nesting
    lines = md_content.split('\n')
    processed_lines = []
    for line in lines:
        if re.match(r'^  [-*+\d]', line) or re.match(r'^   [-*+\d]', line):
            line = '    ' + line.lstrip()
        processed_lines.append(line)
    md_content = '\n'.join(processed_lines)

    # Subscript: ~text~ (but not ~~ which is strikethrough)
    md_content = re.sub(r"(?<!~)~(?!~)(.+?)(?<!~)~(?!~)", r"<sub>\1</sub>", md_content, flags=re.DOTALL)
    # Strikethrough: ~~text~~
    md_content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', md_content, flags=re.DOTALL)
    # Highlight: ==text==
    md_content = re.sub(r'==(.*?)==', r'<mark>\1</mark>', md_content, flags=re.DOTALL)

    html_content = markdown.markdown(
        md_content,
        extensions=[
            'extra',
            'footnotes',
            'fenced_code',
            'codehilite',
            'tables',
            'nl2br',
            'pymdownx.emoji',
        ],
        extension_configs={
            'pymdownx.emoji': {
                'emoji_index': emoji.twemoji,
                'emoji_generator': emoji.to_svg,
            }
        }
    )

    # Post-process rendered HTML to convert task list markers into checkboxes.
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

    # Post-process: superscript ^text^ after markdown processing
    html_content = re.sub(r'\^(.+?)\^', r'<sup>\1</sup>', html_content, flags=re.DOTALL)

    return html_content


class MarkdownHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            client = f"{self.client_address[0]}:{self.client_address[1]}"
        except Exception:
            client = str(self.client_address)
        print(f"Request: {self.command} {self.path} from {client}")

        if self.path == "/":
            markdown_files = [f for f in os.listdir(".") if f.endswith(".md")]
            file_buttons = "".join(
                f"<button onclick=\"location.href='{f}'\">{f}</button>" for f in markdown_files
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
                        background: #0b0b0f;
                        color: #e8e8e8;
                        padding: 1em;
                        max-width: 1200px;
                        margin: auto;
                    }}
                    a {{ color: #89b4ff; }}
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
                        background-color: #2b2b3a;
                        color: #f5f5f5;
                        border: 1px solid #3d3d52;
                        border-radius: 6px;
                    }}
                    button:hover {{
                        background-color: #3a3a4d;
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
                        background-color: #1f1f27;
                        color: #f8f8f2;
                        border-radius: 3px;
                        font-family: monospace;
                        padding: 0.15em 0.3em;
                    }}
                    pre {{
                        background-color: #1f1f27;
                        color: #f8f8f2;
                        border-radius: 6px;
                        overflow-x: auto;
                        padding: 0.8em;
                    }}
                    .codehilite {{
                        background-color: #1f1f27;
                        color: #e8e8e8;
                        padding: 1em;
                        border-radius: 6px;
                        overflow-x: auto;
                    }}
                    del {{
                        color: #a9a9a9;
                    }}
                    mark {{
                        background-color: #665c00;
                        color: #fff7c2;
                        padding: 0.1em 0.2em;
                    }}
                    sup {{
                        font-size: 0.8em;
                        vertical-align: super;
                    }}
                    sub {{
                        font-size: 0.8em;
                        vertical-align: sub;
                    }}
                    .twemoji {{
                        height: 1.2em;
                        width: 1.2em;
                        vertical-align: text-bottom;
                    }}
                    span {{
                        transition: background-color 0.2s ease;
                    }}
                    input[type="checkbox"]:checked + span {{
                        text-decoration: line-through;
                        background-color: #1c1c22;
                    }}
                </style>
                <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    var checkboxes = document.querySelectorAll("input[type='checkbox']");
                    checkboxes.forEach(function(checkbox) {{
                        checkbox.addEventListener("change", function() {{
                            var span = checkbox.nextElementSibling;
                            if (checkbox.checked) {{
                                span.style.textDecoration = "line-through";
                                span.style.backgroundColor = "#1c1c22";
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
            self.wfile.write(html_response.encode("utf-8"))
            return

        if self.path.endswith(".md"):
            raw = self.path[1:]
            file_path = unquote(raw)
            abs_path = os.path.abspath(file_path)
            exists = os.path.exists(abs_path)
            print(f"Resolved path: '{file_path}' -> '{abs_path}', exists={exists}")
            if exists and abs_path.startswith(os.path.abspath(".")):
                html_content = render_markdown_file(abs_path)
                html_response = self.render_page(html_content, file_path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_response.encode("utf-8"))
                return
            msg = f"File Not Found: requested={file_path} resolved={abs_path} exists={exists}"
            print(msg)
            self.send_error(404, msg)
            return

        return super().do_GET()

    def render_page(self, html_content: str, file_name: str) -> str:
        markdown_files = [f for f in os.listdir(".") if f.endswith(".md")]
        file_buttons = "".join(
            f"<button onclick=\"location.href='{f}'\">{f}</button>" for f in markdown_files
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
                    background: #0b0b0f;
                    color: #e8e8e8;
                    padding: 1em;
                    max-width: 1200px;
                    margin: auto;
                }}
                a {{ color: #89b4ff; }}
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
                    background-color: #2b2b3a;
                    color: #f5f5f5;
                    border: 1px solid #3d3d52;
                    border-radius: 6px;
                }}
                button:hover {{
                    background-color: #3a3a4d;
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
                    background-color: #1f1f27;
                    color: #f8f8f2;
                    border-radius: 3px;
                    font-family: monospace;
                    padding: 0.15em 0.3em;
                }}
                pre {{
                    background-color: #1f1f27;
                    color: #f8f8f2;
                    border-radius: 6px;
                    overflow-x: auto;
                    padding: 0.8em;
                }}
                .codehilite {{
                    background-color: #1f1f27;
                    color: #e8e8e8;
                    padding: 1em;
                    border-radius: 6px;
                    overflow-x: auto;
                }}
                .codehilite code {{
                    background: transparent;
                    color: inherit;
                    border: none;
                    padding: 0;
                }}
                del {{
                    color: #a9a9a9;
                }}
                mark {{
                    background-color: #665c00;
                    color: #fff7c2;
                    padding: 0.1em 0.2em;
                }}
                sup {{
                    font-size: 0.8em;
                    vertical-align: super;
                }}
                sub {{
                    font-size: 0.8em;
                    vertical-align: sub;
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
                    background: #11111a;
                }}
                th, td {{
                    border: 1px solid #333;
                    padding: 0.75em;
                    text-align: left;
                    color: #e8e8e8;
                }}
                th {{
                    background-color: #1a1a24;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #13131d;
                }}
                span {{
                    transition: background-color 0.2s ease;
                }}
                input[type="checkbox"]:checked + span {{
                    text-decoration: line-through;
                    background-color: #1c1c22;
                }}
            </style>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    var checkboxes = document.querySelectorAll("input[type='checkbox']");
                    checkboxes.forEach(function(checkbox) {{
                        checkbox.addEventListener("change", function() {{
                            var span = checkbox.nextElementSibling;
                            if (checkbox.checked) {{
                                span.style.textDecoration = "line-through";
                                span.style.backgroundColor = "#1c1c22";
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
    port = 8008
    print(f"Starting server on http://localhost:{port}")
    httpd = HTTPServer(("0.0.0.0", port), MarkdownHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    check_and_install_markdown()
    start_server()
