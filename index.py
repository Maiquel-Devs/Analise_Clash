import requests
import time
import os 
from collections import defaultdict

# Importações da biblioteca para gerar o PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- CONFIGURAções ---
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJjMGZhMDZmLWExNDYtNDk0OC05OTdiLTE1Y2M5ZTRjMGIwYiIsImlhdCI6MTc1OTc4MTI1OSwic3ViIjoiZGV2ZWxvcGVyL2ViOTczZmIwLTEwYjQtMjM5Yi0zNWZjLTFlODQ0MDc4ZWYwYSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS4yMjIuMjM4LjE1NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.PWK_oSiYMXEs0WLzOx5Ju2BeaORpuSePI4v0seYuCyoMsyFaHeLiViPoHb41trpB6oSdbN3B3344jYmJktFKSQ"
CLAN_TAG = "#2G9CPRO90"
PDF_FILENAME = "relatorio_clan.pdf"
IMAGE_FOLDER = "imagens"
# --- FIM DAS CONFIGURAÇÕES ---

HEADERS = { "Authorization": f"Bearer {TOKEN}" }

def url_encode_tag(tag):
    return tag.replace('#', '%23')

def get_player_details(player_tag):
    url = f"https://api.clashofclans.com/v1/players/{url_encode_tag(player_tag)}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def fetch_all_player_data(clan_tag):
    """Busca a lista de membros e depois os detalhes de cada um."""
    url = f"https://api.clashofclans.com/v1/clans/{url_encode_tag(clan_tag)}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"!!! Erro ao buscar lista de membros: {response.text}")
        return None, "Erro"

    clan_data = response.json()
    member_list = clan_data.get('memberList', [])
    clan_name = clan_data.get('name', "N/A")
    
    if not member_list:
        return [], clan_name

    all_player_stats = []
    total_members = len(member_list)
    print(f">>> Iniciando busca detalhada de {total_members} membros para o clã {clan_name}...")

    for i, member in enumerate(member_list, 1):
        player_tag = member.get('tag')
        player_name = member.get('name')
        print(f"    ({i}/{total_members}) Buscando dados de: {player_name}")
        
        player_data = get_player_details(player_tag)
        if player_data:
            heroes = {h['name']: h['level'] for h in player_data.get('heroes', []) if h.get('village') == 'home'}
            all_player_stats.append({
                'name': player_name,
                'townHallLevel': player_data.get('townHallLevel', 0),
                'warStars': player_data.get('warStars', 0),
                'bestTrophies': player_data.get('bestTrophies', 0),
                'king': heroes.get('Barbarian King', 0),
                'queen': heroes.get('Archer Queen', 0),
                'warden': heroes.get('Grand Warden', 0),
                'champion': heroes.get('Royal Champion', 0),
            })
        time.sleep(0.1)
    
    return all_player_stats, clan_name

def create_pdf_report(player_data, clan_name):
    """Cria o documento PDF com os dados processados."""
    if not player_data:
        print("Nenhum dado de jogador para gerar o PDF.")
        return

    print(">>> Gerando o arquivo PDF...")
    doc = SimpleDocTemplate(PDF_FILENAME, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f"Relatório do Clã: {clan_name}", styles['h1'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    summary_title = Paragraph("Resumo de Centros de Vila (CV)", styles['h2'])
    story.append(summary_title)
    
    cv_counts = defaultdict(int)
    for player in player_data:
        cv_counts[player['townHallLevel']] += 1
    
    summary_data = [["Nível do CV", "Quantidade de Jogadores"]]
    for cv_level in sorted(cv_counts.keys(), reverse=True):
        summary_data.append([f"CV {cv_level}", str(cv_counts[cv_level])])

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey), ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12), ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))

    list_title = Paragraph("Detalhes dos Jogadores", styles['h2'])
    story.append(list_title)

    sorted_players = sorted(player_data, key=lambda x: (x['townHallLevel'], x['warStars']), reverse=True)
    
    player_table_data = []
    for player in sorted_players:
        # --- MUDANÇA AQUI: Adicionado o caminho da pasta 'imagens' ---
        image_path = os.path.join(IMAGE_FOLDER, f"CV{player['townHallLevel']}.png")
        
        try:
            cv_image = Image(image_path, width=0.8*inch, height=0.8*inch)
        except Exception as e:
            # Se o arquivo de imagem não for encontrado, usa um texto no lugar
            print(f"Aviso: Não foi possível encontrar a imagem {image_path}. Usando texto no lugar.")
            cv_image = Paragraph(f"CV {player['townHallLevel']}", styles['Normal'])

        player_info_text = f"""
            <b>{player['name']}</b><br/>
            CV: {player['townHallLevel']} | ⭐ Estrelas: {player['warStars']} | 🏆 Recorde: {player['bestTrophies']}<br/>
            Heróis: Rei:{player['king']} | Rainha:{player['queen']} | Guardião:{player['warden']} | Campeã:{player['champion']}
        """
        player_info_paragraph = Paragraph(player_info_text, styles['Normal'])
        
        player_table_data.append([cv_image, player_info_paragraph])

    player_table = Table(player_table_data, colWidths=[1*inch, 6*inch])
    player_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('LEFTPADDING', (1,0), (1,-1), 10), ('RIGHTPADDING', (0,0), (0,-1), 10),
    ]))
    story.append(player_table)

    doc.build(story)
    print(f"\n>>> PDF '{PDF_FILENAME}' criado com sucesso !")

def main():
    player_data, clan_name = fetch_all_player_data(CLAN_TAG)
    if player_data:
        create_pdf_report(player_data, clan_name)

if __name__ == "__main__":
    main()