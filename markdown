# Markdown Syntax Examples

## Basic Syntax

### Headings
# Heading 1
## Heading 2
### Heading 3

### Bold and Italics
**This text is bold**
*This text is italicized*
**_This text is both bold and italicized_**

### Blockquotes
> This is a blockquote.

### Lists
#### Unordered List
- Item 1
- Item 2
  - Subitem 1
  - Subitem 2

#### Ordered List
1. First item
2. Second item
   1. Subitem 1
   2. Subitem 2

### Code
#### Inline Code
Use the `printf` function to display text.

### Footnote
To insert the footnote in your text, the syntax is [^1] or [^footnote1]. The ^ character followed by an identifier inside brackets [] will create the footnote reference.

Footnote referrence in document
This is some text with a footnote[^1].

Footnote definition at placed at bottom of document
[^1]: footnote info to be associated with footnote

### Strikethrough
~This text is struck through.~~

### Links
https://github.com

### Images
https://markdown-here.com/img/icon256.png

## Extended Syntax

### Tables
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

### Fenced Code Blocks for syntax highlighting
```python
def hello_world():
    print("Hello, world!")
