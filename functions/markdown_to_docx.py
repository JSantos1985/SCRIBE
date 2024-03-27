import pypandoc
import uuid

def markdown_to_docx(markdown_content):
    """
    Converts Markdown content to a DOCX file using pypandoc.

    Parameters:
    - markdown_content (str): The Markdown-formatted string.
    - output_filename (str): The desired filename for the output DOCX file.
    """
    filename = f'{uuid.uuid4()}.docx'
    output = pypandoc.convert_text(markdown_content, 'docx', format='md', outputfile=filename, extra_args=['-RTS'])
    if output:
        print(output)
    else:
        print(f"DOCX file created at: {filename}")