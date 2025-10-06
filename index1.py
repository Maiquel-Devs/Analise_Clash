import requests
import time

# Use o seu TOKEN mais recente e válido
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJjMGZhMDZmLWExNDYtNDk0OC05OTdiLTE1Y2M5ZTRjMGIwYiIsImlhdCI6MTc1OTc4MTI1OSwic3ViIjoiZGV2ZWxvcGVyL2ViOTczZmIwLTEwYjQtMjM5Yi0zNWZjLTFlODQ0MDc4ZWYwYSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS4yMjIuMjM4LjE1NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.PWK_oSiYMXEs0WLzOx5Ju2BeaORpuSePI4v0seYuCyoMsyFaHeLiViPoHb41trpB6oSdbN3B3344jYmJktFKSQ"

CLAN_TAG = "#2G9CPRO90"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def url_encode_tag(tag):
    """Converte a tag # para o formato de URL."""
    return tag.replace('#', '%23')

def get_clan_members(clan_tag):
    """Busca apenas a lista de membros do clã."""
    url = f"https://api.clashofclans.com/v1/clans/{url_encode_tag(clan_tag)}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('memberList', [])
    else:
        print(f"!!! Erro ao buscar a lista de membros: {response.status_code} - {response.text}")
        return None

def get_player_details(player_tag):
    """Busca os detalhes de um jogador específico."""
    url = f"https://api.clashofclans.com/v1/players/{url_encode_tag(player_tag)}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        # Retorna None se houver erro para não parar o script
        return None

def main():
    print(f">>> Buscando lista de membros do clã {CLAN_TAG}...")
    member_list = get_clan_members(CLAN_TAG)
    
    if not member_list:
        print("Não foi possível obter a lista de membros.")
        return

    detailed_player_stats = []
    total_members = len(member_list)
    
    print(f">>> Iniciando busca detalhada de {total_members} membros. Isso pode levar um momento...")

    # Loop para buscar os detalhes de cada jogador
    for i, member in enumerate(member_list, 1):
        player_tag = member.get('tag')
        player_name = member.get('name')
        print(f"    ({i}/{total_members}) Buscando dados de: {player_name}")
        
        player_data = get_player_details(player_tag)
        
        if player_data:
            detailed_player_stats.append({
                'name': player_data.get('name'),
                'warStars': player_data.get('warStars', 0),
                'bestTrophies': player_data.get('bestTrophies', 0)
            })
        else:
            print(f"    !!! Falha ao buscar dados para {player_name} ({player_tag})")
        
        # Pequena pausa para não sobrecarregar a API
        time.sleep(0.1)

    if not detailed_player_stats:
        print("Nenhuma estatística detalhada pôde ser coletada.")
        return

    # --- Seção de Rankings ---
    print("\n" + "="*50)
    print("              RANKINGS E ESTATÍSTICAS")
    print("="*50)

    # Ranking por Estrelas de Guerra
    top_war_stars = sorted(detailed_player_stats, key=lambda x: x['warStars'], reverse=True)
    print("\n--- RANKING POR ESTRELAS DE GUERRA TOTAIS ---")
    for idx, player in enumerate(top_war_stars, 1):
        print(f"  {idx}. {player['name']} - {player['warStars']} estrelas")

    # Ranking por Recorde de Troféus
    top_trophies = sorted(detailed_player_stats, key=lambda x: x['bestTrophies'], reverse=True)
    print("\n--- RANKING POR RECORDE DE TROFÉUS ---")
    for idx, player in enumerate(top_trophies, 1):
        print(f"  {idx}. {player['name']} - {player['bestTrophies']} troféus")


if __name__ == "__main__":
    main()