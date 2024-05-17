
import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
from fastapi.responses import Response
import json
import os
from utils.utils import * 
new_request_cimg = os.environ.get("CC_URL_CIMG")
new_request_cod = os.environ.get("CC_URL_COD")


def generate_pdf_generic_logic(api_key, idMember, idVerification):
    
    headers = {
        "API-Key": api_key
    }
    params = {
        "idMember": idMember,
        "idVerification": idVerification
    }
    try:
        response = requests.get(new_request_cod+'/v1/profile/validation/hook/detail', headers=headers, params=params)
        if response.status_code == 200:
            data_master = response.json()
        else:
            return Response(content="Error al obtener los datos", status_code=response.status_code)
    except Exception as e:
        return Response(content=f"Error generating PDF: {e}", status_code=500)

    client_data = data_master.get("data", {})
    _achievements = client_data.get("verificationData", {})
    achievements = _achievements.get("achievements", [])
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    id_verif = client_data.get("idVerificationTemplate", "")
    y_position  = 630  # Starting Y position for the content
    y_position_val = 630
    #se setea al id particular para ficha generica
    if id_verif == '646cc5fefd4cb6374cc951e2':
        c.drawString(270, y_position + 120, f"Ficha Genérica".upper())
    generate_membrete_from_json(c, data_json, x_membret, y_membret)
    draw_borders(c)
    json_data={}
    #json_pdf_data={}
    datos={}
    pdf_data={}
    #se realiza lo siguiente para tomar en cuenta cuando los datos vengan desordenados. simplemente estamos dando un orden de posicionamiento.
    list_achivs = ['DATOS PERSONALES', 'DATOS DE DIRECCIÓN', 'INFORMACIÓN DE EMPLEO', 'Información personal adicional', 'Listas de vigilancia','PEP','Declaración jurada']

    for achivs in list_achivs:
    # Buscar el JSON correspondiente al achivs actual
        actual_json = None
        for item in achievements:
            if item['achievement_name'].upper() == achivs.upper():
                actual_json = item
                break

        if actual_json:
            achievement = item
            c.setFillColorRGB(0.4, 0.4, 0.4)  # Darker gray color for background
            c.rect(content_x, y_position, content_width, 25, fill=1)
            achievement_name = achievement.get("achievement_name")
            c.setFillColorRGB(1, 1, 1)  # White color for text
            c.setFont("Helvetica", 12)
            c.drawCentredString(297, y_position + 10, achievement_name.upper()) # Title of Achievement
            requirements = achievement.get("requirements", [])
            y_position -= 20 # decrementamos porque ya usamos el valor inicial para colocar el titulo. ahora queremos colocar los achivss
            y_position_val -= 20
            # Check if the content is overflowing the page
            if y_position < 40:
                c.showPage()  # Add a new page
                generate_membrete_from_json(c, data_json, x_membret, y_membret) 
                draw_borders(c)
                c.drawString(250, 730, f"Pdf Prueba CC")
                y_position = 630  # Reset Y position
                y_position_val = 630

            x_position = content_x
            x_ult_value= x_ult_title=10
            y_position_line = y_position
            delta = 10
            aux_y=y_position
            
            for requirement in requirements:
                c.setFillColorRGB(0, 0, 0)  # Color negro
                requirement_name = requirement.get("requirement_name").upper() #Titulo
                value = requirement.get("latest_approved", {}).get("value", "") #valor
                default_val = max(x_ult_title, x_ult_value) + delta
                verif_title = get_last_position(default_val, f"{requirement_name}", "Helvetica", 12)
                verif_value = get_last_position(default_val, f"{value}", "Helvetica", 12)
                
                if verif_title >= content_width or verif_value >= content_width:
                    x_ult_title=x_ult_value=10
                    y_position_line-=40
                    delta=10
                x_position_defa = max(x_ult_title, x_ult_value)
                
                c.setFont("Helvetica-Bold",12)
                #si el valor del contenido es la url de una imagen, obviamos la escritura del texto en el PDF y apilamos en una lista para luego ser 
                #insertada mas adelante
                if type(value)!=bool and is_file_type(value, 'image'):
                        datos[requirement_name] = value
                        # Convertir el diccionario a formato JSON
                        json_data = json.dumps(datos)
                elif type(value)!=bool and is_file_type(value, 'pdf'):
                        pdf_data[requirement_name] = value
                else:
                    c.drawString(x_position_defa + delta, y_position_line, f"{requirement_name.upper()}:")
                    y_position -= 20
                    aux_y-=20
                    y_position_line-=20
                    c.setFont("Helvetica",12)
                    if type(value)!=bool:
                        value=value.upper()
                    c.drawString(x_position_defa + delta, y_position_line, f"{value}")
                    c.line(x_position,y_position_line-5, content_width+10, y_position_line -5)
                    default_val = max(x_ult_title, x_ult_value)
                    x_ult_title = get_last_position(default_val, f"{requirement_name}", "Helvetica", 12)
                    x_ult_value = get_last_position(default_val, f"{value}", "Helvetica", 12)
                    y_position_line+=20
                    delta+=10
                    y_position -=20
                    aux_y-=20
            y_position=y_position_line-50
        datos_u = json.loads(json_data)
    #creacion de hojas del pdf para las imagenees
    folder_name = "files"
    i=0
    for key, value in datos_u.items():
        c.showPage()
        c.drawString(x_position_defa + delta, y_position_line, f"{value}")
        params = {
            "urlName":value
        }
        try:
            response = requests.get(new_request_cimg+'/v1/file', headers=headers, params=params)

            if response.status_code == 200:
                response_json = response.json()
                file_data = response_json.get('data', {}).get('file', {})
                buffer_data = file_data.get('data', [])
        
                # Convertir los datos del buffer en bytes
                bytes_data = bytes(buffer_data)
                # Crear la carpeta 'files' si no existe
   
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Obtener la fecha y hora actual para usar como nombre de archivo
                img_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(i)
                # Construir la ruta completa del archivo
                file_path = os.path.join(folder_name, img_name + ".jpg")

                # Continuar con tu lógica para trabajar con los datos de bytes, por ejemplo, guardarlos en un archivo
                with open(file_path, "wb") as f:
                    f.write(bytes_data)
                    add_image(c, file_path, x_image, y_image, width_image, height_image)
                i+=1
        except Exception as e:
            return Response(content=f"Error generating PDF: {e}", status_code=500)
    #se agregan los pdfs encontrados
    pdfse = c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    # Guardar el PDF generado con Canvas como "canvas.pdf"

    # Abrir el PDF generado con Canvas
    if pdf_data:
        for key, value in pdf_data.items():
            # Guardar el PDF generado con Canvas
            canvas_pdf_path = key + "_canvas.pdf"
            with open(canvas_pdf_path, "wb") as f:
                f.write(pdf_bytes)
            
            # Crear el PdfWriter para combinar PDFs
            pdf_writer = PdfWriter()
            
            # Agregar el PDF generado con Canvas
            pdf_writer.append(PdfReader(canvas_pdf_path))
            
            # Agregar el otro PDF
            pdf_writer.append(PdfReader(value))
            
            # Guardar el PDF combinado
            result_pdf_path = key + "_result.pdf"
            pdf_writer.write(result_pdf_path)
            pdf_writer.close()
            
            # Leer el PDF combinado para la respuesta
            with open(result_pdf_path, "rb") as f:
                pdf_bytes = f.read()
    return Response(content=pdf_bytes, media_type="application/pdf")