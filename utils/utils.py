from reportlab.pdfbase import pdfmetrics
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

data_master=''
# Define el tamaño y posición del contenido
content_width =590
content_height = 670
content_x = 10
content_y = -15
x_image = 8.5/4
y_image = 11/4
width_image = 500
height_image = 500
x_membret = 425
y_membret = 765


data_json = {
"LUGAR": "VENEZUELA",
"FECHA DE ELABORACIÓN": "2024-05-10",
"CÓDIGO CLIENTE": "FRANKRO22"
}



def get_last_position(x_position, text, font, font_size):
    """
    Calculate the x-coordinate of the last character in a string when rendered.

    Args:
        x_position (float): The starting x-coordinate.
        text (str): The text string to be measured.
        font (str): The name of the font used.
        font_size (float): The size of the font.

    Returns:
        float: The x-coordinate of the last character in the string.
    """
    text_width = pdfmetrics.stringWidth(text + ':', font, font_size)
    x_last_char = x_position + text_width
    return x_last_char

def create_membrete(x, y, key, value, canvas):
    """
    Draw a key-value pair on a canvas at specified coordinates.

    Args:
        x (float): The x-coordinate where the key-value pair starts.
        y (float): The y-coordinate where the key-value pair starts.
        key (str): The key part of the key-value pair.
        value (str): The value part of the key-value pair.
        canvas (Canvas): The canvas object from the reportlab library.
    """
    canvas.drawString(x, y, key + ":")
    canvas.drawString(x, y - 20, value)

def generate_membrete_from_json(canvas, input_json, x_membrete, y_membrete):
    """
    Generate a membrete (header) from a JSON object and draw it on a canvas.

    Args:
        canvas (Canvas): The canvas object from the reportlab library.
        input_json (dict): The input JSON object containing key-value pairs.
        x_membrete (float): The starting x-coordinate for the membrete.
        y_membrete (float): The starting y-coordinate for the membrete.
    """
    for key, value in input_json.items():
        create_membrete(x_membrete, y_membrete, key, value, canvas)
        y_membrete -= 40

        

def draw_borders(canvas):
    """
    Draws borders around the content area on a canvas.

    Args:
        canvas (Canvas): The canvas object from the reportlab library.
        content_x (float): The x-coordinate of the content area.
        content_y (float): The y-coordinate of the content area.
        content_width (float): The width of the content area.
        content_height (float): The height of the content area.
    """
    # Draw the border of the content
    canvas.setStrokeColorRGB(0, 0, 0)  # Set line color to black
    canvas.setLineWidth(0.3)  # Set line width

    # Draw top and bottom horizontal lines
    canvas.line(content_x, content_y + content_height, content_x + content_width, content_y + content_height)
    canvas.line(content_x, content_y + 20, content_x + content_width, content_y + 20)
    
    # Draw left and right vertical lines
    canvas.line(content_x, content_y + 20, content_x, content_y + content_height)
    canvas.line(content_x + content_width, content_y + 20, content_x + content_width, content_y + content_height)

def add_image(canvas, image_path, x, y, width, height):
    """
    Adds an image to the canvas at specified coordinates.

    Args:
        canvas (Canvas): The canvas object from the reportlab library.
        image_path (str): The path to the image file.
        x (float): The x-coordinate where the image will be placed.
        y (float): The y-coordinate where the image will be placed.
        width (float): The width of the image.
        height (float): The height of the image.
    """
    try:
        canvas.drawImage(image_path, x, y, width, height)
    except Exception as e:
        # If the image cannot be loaded, draw a placeholder with "Image Not Found"
        canvas.rect(x, y, width, height)
        canvas.drawString(x + 5, y + 5, "Image Not Found")
        print(f"Error loading image: {e}")

def is_file_type(file_path, file_type):
    """
    Checks if the given file path has the specified file extension type.

    Args:
        file_path (str): The file path to check.
        file_type (str): The type of file to check for ('image' or 'pdf').

    Returns:
        bool: True if the file has the specified extension, False otherwise.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    pdf_extension = '.pdf'
    extension = Path(file_path).suffix.lower()
    
    if file_type == 'image':
        return extension in image_extensions
    elif file_type == 'pdf':
        return extension == pdf_extension
    else:
        raise ValueError("Invalid file type specified. Use 'image' or 'pdf'.")


def merge_pdfs(output_pdf_path, pdf_list):
    pdf_writer = PdfWriter()

    for pdf in pdf_list:
        try:
            pdf_reader = PdfReader(pdf)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
        except Exception as e:
            print(f"Error reading PDF: {pdf}, {e}")

    with open(output_pdf_path, 'wb') as out:
        pdf_writer.write(out)