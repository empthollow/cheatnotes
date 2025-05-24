# Markdown Server Project

This project is a simple HTTP server that serves an HTML page listing all Markdown (.md) files in the directory. Users can select a Markdown file to view its content rendered as HTML.

## Project Structure

```
markdown_server_project
├── src
│   ├── server.py          # Main script to start the HTTP server
│   └── templates
│       └── index.html     # HTML template for displaying Markdown files
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Requirements

This project requires the following Python package:

- `markdown`: A library to convert Markdown files to HTML.

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Navigate to the project directory:

   ```
   cd markdown_server_project
   ```

2. Start the server:

   ```
   python src/server.py
   ```

3. Open your web browser and go to `http://localhost:8000` to view the list of Markdown files.

4. Click on any Markdown file to render its content.

## License

This project is open-source and available under the MIT License.