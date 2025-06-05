import json
import time 
from google import genai
import dotenv
import os
from pydantic import BaseModel, Field
from typing import List, Tuple # Tuple is still fine for Python type hinting

# class VideoAnalysis(BaseModel):
#     assunto_principal: str
#     secoes_chaves_com_timestamps: list[tuple[str, str]] 
#     exercicios: list[str]
#     tags: list[str]


# Define a model for your timestamped section
class SecaoComTimestamp(BaseModel):
    nome_da_secao: str = Field(..., description="O nome ou título da seção chave identificada no vídeo.")
    timestamp: str = Field(..., description="O timestamp de início da seção no formato HH:MM:SS ou MM:SS.")

class VideoAnalysis(BaseModel):
    assunto_principal: str = Field(..., description="O tema central ou assunto principal abordado no vídeo.")
    secoes_chaves_com_timestamps: List[SecaoComTimestamp] = Field(
        ...,
        description="Uma lista de seções/capítulos importantes do vídeo, cada uma com seu nome e timestamp de início."
    )
    exercicios: List[str] = Field(
        default_factory=list, # Use default_factory if it can be empty
        description="Sugestões de exercícios ou atividades práticas baseadas no conteúdo do vídeo."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Uma lista de palavras-chave ou tags relevantes que categorizam o conteúdo do vídeo."
    )

class Aula(BaseModel):
    titulo_da_aula: str
    video_url: str
    analysis: VideoAnalysis

def get_client():
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)

def upload_video(file_path, client):

    print(f"Uploading file: {file_path}...")

    # 1. Start the upload
    # Use upload_file for clarity and potentially better handling
    # Note: client.files.upload is valid, but upload_file is often recommended
    # Let's stick with your original method for minimal changes first:
    # myfile_upload_response = client.files.upload_file(path=file_path, display_name="My Video for Summarization")

    # Or using your original code (result is similar):
    myfile_upload_response = client.files.upload(file=file_path)

    print(f"File uploaded: {myfile_upload_response.name}, State: {myfile_upload_response.state}")
    print("Waiting for file to become ACTIVE...")

    # 2. Poll for ACTIVE state
    file_id = myfile_upload_response.name
    check_interval_seconds = 10 # How often to check (in seconds)
    max_wait_time_seconds = 300 # Maximum time to wait (e.g., 5 minutes)
    start_time = time.time()

    while True:
        # Get the current status of the file
        myfile_status = client.files.get(name=file_id)
        print(f"Current file state: {myfile_status.state}")

        if myfile_status.state == genai.types.FileState.ACTIVE:
            print("File is ACTIVE. Proceeding with content generation.")
            myfile = myfile_status # Use the full file object which is now ACTIVE
            break
        elif myfile_status.state == genai.types.FileState.FAILED:
            raise ValueError(f"File processing failed: {myfile_status.state}")
        elif time.time() - start_time > max_wait_time_seconds:
            raise TimeoutError(f"File did not become ACTIVE within {max_wait_time_seconds} seconds.")

        # Wait before checking again
        time.sleep(check_interval_seconds)
    return myfile

def analyze_video(prompt, file_path, client) -> Aula:
    print("Generating content...")
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash-preview-05-20", 
            contents = [file_path, prompt], 
            config = {
                "response_mime_type": "application/json",
                "response_schema": VideoAnalysis,
            },
        )

        aula = Aula(
            titulo_da_aula=file_path.name,
            video_url="",  
            analysis=response.parsed
        )
        
        return aula

    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        print(f"Deleting file {file_path.name} due to error...")
        client.files.delete(name=file_path.name)
        return Aula(
            titulo_da_aula=file_path.name if hasattr(file_path, "name") else str(file_path),
            video_url="",
            analysis=VideoAnalysis(
                assunto_principal="",
                secoes_chaves_com_timestamps=[],
                exercicios=[],
                tags=[]
            )
        )


def save_analysis_to_jsonl(analysis: Aula, filename: str):
    """
    Appends a single Aula object as a JSON line to the specified file.
    """
    try:
        # 'a' mode opens the file for appending.
        # If the file does not exist, it creates it.
        with open(filename, "a", encoding="utf-8") as f:
            f.write(analysis.model_dump_json() + "\n")
        print(f"Successfully saved analysis. ")
    except IOError as e:
        print(f"Error saving analysis : {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving: {e}")


    

def is_title_in_jsonl(title, jsonl_path):
    if not os.path.exists(jsonl_path):
        return False
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("titulo_da_aula") == title:
                    return True
            except Exception:
                continue
    return False