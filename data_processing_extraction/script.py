import os 

from utils import (
    get_client, 
    upload_video, 
    analyze_video, 
    save_analysis_to_jsonl, 
    is_title_in_jsonl
)


client = get_client()

prompt = """
Sou guitarrista de 7 cordas e estou usando este vídeo como tutorial. 
Gere um resumo bem completo e detalhado para me ajudar a estudar eficientemente.
O resumo deve funcionar como uma ficha de revisão rápida.
O nome do professor é "Gian Correa"

Aqui está o que desejo incluir:
* **Título/Assunto Principal:** Qual é o objetivo geral da lição?
* **Quebra por Seções com timestamps** : lista de pontos chaves para Fixar, i.e. os 2 ou 3 elementos mais importantes da lição.
* **Lista de exercicios** : Quais exercícios devo praticar para fixar o conteúdo?
* **Tags:** Quais tags são relevantes para este vídeo? (por exemplo, "técnica de mao esquera", "arpejos", "escalas", "percepçao", etc.)

Use este modelo para estruturar o resumo:
** assunto_principal** 
**secoes_chaves_com_timestamps**
**exercicios**
**tags**

Certifique-se de que o resumo capture a essência de cada parte importante do vídeo.
O objetivo é conseguir reler este resumo e saber exatamente o que praticar sem ter que reassistir o vídeo inteiro.
"""

VIDEOS_FOLDER = "videos"
OUTPUT_FILE_JSONL = "video_analysis.jsonl"

video_files = [VIDEOS_FOLDER + '/' + f for f in os.listdir(VIDEOS_FOLDER) if f.endswith(".mp4")]

# List of video URLs
video_files = [
    ("https://youtu.be/EspLvzAb22M", "Módulo 2 ｜ semana 1 ｜ aula 1"),
    ("https://youtu.be/6BrqGl9rIK0", "Módulo 2 ｜ semana 1 ｜ aula 2"),
    ("https://youtu.be/RRrf6_VpGz8", "Módulo 2 ｜ semana 2 ｜ aula 1"),
    ("https://youtu.be/hV-WhybKilg", "Módulo 2 ｜ semana 2 ｜ aula 2"),
    ("https://youtu.be/Iw-C6QMXdGc", "Módulo 2 ｜ semana 3 ｜ aula 1"),
    ("https://youtu.be/tGo6Wy9lZv0", "Módulo 2 ｜ semana 3 ｜ aula 2"),
    ("https://youtu.be/zBihFcDwzgk", "Módulo 2 ｜ semana 4 ｜ aula 1"),
    ("https://youtu.be/MmqKkcVRd1w", "Módulo 2 ｜ semana 4 ｜ aula 2"),
    ("https://youtu.be/RT3HE5rEiKo", "Módulo 2 ｜ semana 5 ｜ aula1"),
    ("https://youtu.be/nKT1gvQGir4", "Módulo 2 ｜ semana 5 ｜ aula 2"),
    ("https://youtu.be/monCTqmAAOQ", "Módulo 2 ｜ semana 6 ｜ aula 1"),
    ("https://youtu.be/DPdcOodwh0s", "Módulo 2 ｜ semana 6 ｜ aula 2"),
    ("https://youtu.be/4MgKyR19kMg", "Módulo 2 ｜ semana 7 ｜ aula 1"),
    ("https://youtu.be/Zg_81fObFIw", "Módulo 2 ｜ semana 7 ｜ aula 2"),
    ("https://youtu.be/X1KAglEK_Ig", "Módulo 2 ｜ semana 8 ｜ aula 2"),
    ("https://youtu.be/vypk3Kq3N_Q", "Módulo 2 ｜ semana 8 ｜ aula 1"),
    ("https://youtu.be/CvyoUf1QzTg", "Módulo 3 ｜ semana 1 ｜ aula 1"),
    ("https://youtu.be/Mc7aeNvEZNk", "Módulo 3 ｜ semana 1 ｜ aula 2"),
    ("https://youtu.be/MOu_fjohOg0", "Módulo 3 ｜ semana 2 ｜ aula 1"),
    ("https://youtu.be/YeDHA1IvkJQ", "Módulo 3 ｜ semana 2 ｜ aula 2"),
    ("https://youtu.be/5v84aUFp2tI", "Módulo 3 ｜ semana 3 ｜ aula 1"),
    ("https://youtu.be/YD7ylbYCQ14", "Módulo 3 ｜ semana 3 ｜ aula 2"),
    ("https://youtu.be/Q5prVf_JBJs", "Módulo 3 ｜ semana 4 ｜ aula 2"),
    ("https://youtu.be/-b_Hs0P29hQ", "Módulo 3 ｜ semana 4 ｜ aula 1"),
    ("https://youtu.be/SotwaVnrx44", "Módulo 3 ｜ semana 4 ｜ aula 1 | Aula complementar "),
    ("https://youtu.be/kcm-wi_R_yQ", "Módulo 3 ｜ semana 5 ｜ aula 1"),
    ("https://youtu.be/SgWUyYDmqKI", "Módulo 3 ｜ semana 5 ｜ aula 2"),
    ("https://youtu.be/hEk4RDBIE38", "Módulo 3 ｜ semana 6 ｜ aula 1"),
    ("https://youtu.be/gYkVrXHx-5o", "Módulo 3 ｜ semana 6 ｜ aula 2"),
    ("https://youtu.be/0lA2dih88wo", "Módulo 3 ｜ semana 7 ｜ aula 1"),
    ("https://youtu.be/pMyE-98Z5qc", "Módulo 3 ｜ semana 7 ｜ aula 2"),
    ("https://youtu.be/Sx8kOo9ifYc", "Módulo 3 ｜ semana 8 ｜ aula 2"),
    ("https://youtu.be/xhfniRFDw7Q", "Módulo 3 ｜ semana 8 ｜ aula 1"),
    ("https://youtu.be/0LDedKaUPdY", "Módulo 4 ｜ semana 1 ｜ aula 1"),
    ("https://youtu.be/nb7jn434X9E", "Módulo 4 ｜ semana 1 ｜ aula 2"),
    ("https://youtu.be/ohmlecNS4dk", "Módulo 4 ｜ semana 2 ｜ aula 2"),
    ("https://youtu.be/DSpFjx2Bh2Y", "Módulo 4 ｜ semana 2 ｜ aula 1"),
    ("https://youtu.be/8-AjG9vpjWg?si=d1OL_kHxSilOblYo", "Não escreva! Aula Complementar"),
    ("https://youtu.be/eHsWVd6HHOg", "Módulo 4 ｜ semana 3 ｜ aula 1"),
    ("https://youtu.be/qZ7rol-spP8", "Módulo 4 ｜ semana 3 ｜ aula 2"),
    ("https://youtu.be/2nn9eRjIudM", "Módulo 4 ｜ semana 4 ｜ aula 2"),
    ("https://youtu.be/q4nPTX94X-Y", "Módulo 4 ｜ semana 4 ｜ aula 1"),
    ("https://youtu.be/wXLg88TScYE", "Módulo 4 ｜ semana 5 ｜ aula 1"),
    ("https://youtu.be/644QLZb72Uw", "Módulo 4 ｜ semana 5 ｜ aula 2"),
    ("https://youtu.be/H6KKPdcxq7c", "Módulo 4 ｜ semana 6 ｜ aula 2"),
    ("https://youtu.be/y7JijSqh78M", "Módulo 4 ｜ semana 6 ｜ aula 1"),
    ("https://youtu.be/Z2AbuerLfpE", "Módulo 4 ｜ semana 7 ｜ aula 1"),
    ("https://youtu.be/-IiOQKz8Qj8", "Módulo 4 ｜ semana 7 ｜ aula 2"),
    ("https://youtu.be/fLaZlZMqq6M", "Módulo 4 ｜ semana 8 ｜ aula 1"),
    ("https://youtu.be/11NVhCiDTlo", "Módulo 4 ｜ semana 8 ｜ aula 2"),
    ("https://youtu.be/03bpW0nuqH4", "Módulo 4 ｜ semana 9 ｜ aula única"),
    ("https://youtu.be/ZtHpEY5TXNI", "Módulo 5 ｜ semana 1 ｜ aula 1 ok"),
    ("https://youtu.be/_-7p7N2hV2I", "Módulo 5 ｜ semana 1 ｜ Avançado"),
    ("https://youtu.be/Yl2wDknfIQw", "Módulo 5 ｜ semana 1 ｜ aula 2"),
    ("https://youtu.be/GlecgwSqVew", "Módulo 5 ｜ semana 2 ｜ aula 1"),
    ("https://youtu.be/ErNZzE2KepM", "Módulo 5 ｜ semana 2 ｜ aula 2"),
    ("https://youtu.be/sPVhGECgGbw", "Módulo 5 ｜ semana 2 ｜ avançado"),
    ("https://youtu.be/GiyswAkU238", "Módulo 5 ｜ semana 3 ｜ aula 1"),
    ("https://youtu.be/dfuM6vzeT34", "Módulo 5 ｜ semana 3 ｜ aula 2"),
    ("https://youtu.be/ZjMv-rbaUy4", "Módulo 5 ｜ semana 4 ｜ aula 2"),
    ("https://youtu.be/qKvxOrW3bU8", "Módulo 5 ｜ semana 4 ｜ aula 1"),
    ("https://youtu.be/Y37ZMLAr4xc", "Módulo 5 ｜ semana 2 ｜ aula 1"),
    ("https://youtu.be/EJiiQ6z4wZI", "Módulo 5 ｜ semana 5 ｜ aula 2"),
    ("https://youtu.be/opaN-J16rmI", "Módulo 5 ｜ semana 6 ｜ aula 2"),
    ("https://youtu.be/awdN3Z62-_Y", "Módulo 5 ｜ semana 6 ｜ aula 1"),
    # ("https://youtu.be/4v70zzyqvX4", "Loop Tamborim"),
    ("https://youtu.be/_u_jQEHRykI", "Módulo 5 ｜ semana 7 ｜ aula única"),
]


for youtube_url, file_name in video_files:
    if is_title_in_jsonl(file_name, OUTPUT_FILE_JSONL):
        print(f"Skipping '{file_name}' (already processed)")
        continue
    try:
        file_path = os.path.join(VIDEOS_FOLDER, file_name + ".mp4")
        uploaded_video = upload_video(file_path, client)
        analysis = analyze_video(prompt, uploaded_video, client)
        analysis.video_url = youtube_url
        analysis.titulo_da_aula = file_name
        save_analysis_to_jsonl(analysis, OUTPUT_FILE_JSONL)
        print(analysis)
    except Exception as e:
        print(f"An error occurred while processing '{file_name}': {e} ---> to logs")
        with open("missing.json", "a", encoding="utf-8") as log_file:
            log_file.write(f"{file_name}\n")
        continue
    


    
