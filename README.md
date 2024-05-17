# FastAPI Application

## Description

This is a FastAPI application that provides endpoints for generating PDF files and other related functionalities. The application uses various Python libraries such as ReportLab for PDF generation and PyPDF2 for PDF manipulation.

## Features

- Generate PDF documents dynamically based on provided data.
- Integrate with external services to fetch data.
- Secure API endpoints with external HTTPBearer authentication.

## Requirements

- Python 3.8+
- FastAPI
- ReportLab
- Requests
- PyPDF2

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/jonbandes/pdf_app
    cd pdf_app
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv env
    ```
3. **Environment Variables**

    specially we use:
    ```sh
CC_URL_CIMG=<URL_FOR_CIMG>
CC_URL_COD=<URL_FOR_COD>

    source /etc/environment
    ```

4. **Activate a virtual environment:**

    ```sh
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

5. **Install the dependencies:**

    ```sh
    sudo apt install python3-pip
    pip install -r requirements.txt
    sudo apt install uvicorn
    ```

# Usage
Run the application:

    ```sh
    uvicorn main:app --reload
    ```
## Access the API documentation:

Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation provided by Swagger UI.

## API Endpoints
    Generate PDF
    URL: /generate_pdf
    Method: POST
    Headers:
    API-Key: Your API key for authentication
    Query Parameters:
    idMember: Integer representing the member ID
    idVerification: String representing the verification ID

##### ##### ##################################################

### Aplicación FastAPI

### Descripción

Esta es una aplicación FastAPI que proporciona endpoints para generar archivos PDF y otras funcionalidades relacionadas. La aplicación utiliza varias bibliotecas de Python, como ReportLab para la generación de PDF y PyPDF2 para la manipulación de PDF.

### Características

- Generar documentos PDF dinámicamente basado en los datos proporcionados.
- Integrarse con servicios externos para obtener datos.
- Proteger los endpoints de la API con autenticación HTTPBearer externos.

### Requisitos

- Python 3.8+
- FastAPI
- ReportLab
- Requests
- PyPDF2

### Instalación
1. **Clone the repository:**

    ```sh
    git clone https://github.com/jonbandes/pdf_app
    cd pdf_app
    ```

1. **Clonar el repositorio:**

    ```sh
    git clone https://github.com/tuusuario/tu-nombre-repo.git
    cd tu-nombre-repo
    ```

2. **Crear un entorno virtual:**

    ```sh
    python3 -m venv env
    Variables de Entorno:
    Específicamente usamos:
    
    CC_URL_CIMG=<URL_PARA_CIMG>
    CC_URL_COD=<URL_PARA_COD>

    source /etc/environment
    ```

4. **Activar el entorno virtual:**

 
    ```sh
    source env/bin/activate  # En Windows usar `env\Scripts\activate`
    ```
5. **Instalar las dependencias:**

    ```sh
    sudo apt install python3-pip
    pip install -r requirements.txt
    sudo apt install uvicorn
    ```

### Uso
Ejecutar la aplicación:

    ```sh
    uvicorn main:app --reload
    ```
### Acceder a la documentación de la API:

Abre tu navegador y navega a http://127.0.0.1:8000/docs para ver la documentación interactiva de la API proporcionada por Swagger UI.

### Endpoints de la API

- Generar PDF
- URL: /generate_pdf
- Método: POST
- Headers:
- API-Key: Tu clave API para autenticación
- Parámetros de consulta:
- idMember: Entero que representa el ID del miembro
- idVerification: Cadena que representa el ID de verificación