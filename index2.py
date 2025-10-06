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
    """Busca a lista de membros do clã."""
    url = f"https://api.clashofclans.com/v1/clans/{url_encode_tag(clan_tag)}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        clan_data = response.json()
        print(f">>> Sucesso! Análisando o clã: {clan_data.get('name')}")
        return clan_data.get('memberList', [])
    else:
        print(f"!!! Erro ao buscar a lista de membros: {response.status_code} - {response.text}")
        return None

def get_player_details(player_tag):
    """Busca os detalhes de um jogador específico."""
    url = f"https://api.clashofclans.com/v1/players/{url_encode_tag(player_tag)}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    member_list = get_clan_members(CLAN_TAG)
    if not member_list:
        return

    total_members = len(member_list)
    print(f">>> Iniciando busca detalhada de {total_members} membros. Isso pode levar um momento...")

    role_order = {'leader': 0, 'coLeader': 1, 'admin': 2, 'member': 3}
    sorted_members = sorted(member_list, key=lambda m: role_order.get(m.get('role', 'member'), 4))

    print("\n" + "="*70)
    print("                      RELATÓRIO DE FORÇA E HISTÓRICO")
    print("="*70)
    
    for i, member in enumerate(sorted_members, 1):
        player_tag = member.get('tag')
        player_name = member.get('name')
        
        player_data = get_player_details(player_tag)
        
        if player_data:
            # Nível do Centro de Vila
            th_level = player_data.get('townHallLevel', 0)
            
            # Níveis dos Heróis
            heroes = {h['name']: h['level'] for h in player_data.get('heroes', []) if h.get('village') == 'home'}
            king_lvl = heroes.get('Barbarian King', 0)
            queen_lvl = heroes.get('Archer Queen', 0)
            warden_lvl = heroes.get('Grand Warden', 0)
            champ_lvl = heroes.get('Royal Champion', 0)
            
            # Estatísticas de Guerra e Troféus
            war_stars = player_data.get('warStars', 0)
            best_trophies = player_data.get('bestTrophies', 0)
            
            # Montando a linha de exibição
            heroes_str = f"Rei:{king_lvl} | Rainha:{queen_lvl} | Guardião:{warden_lvl} | Campeã:{champ_lvl}"
            print(f"\n-> {player_name}")
            print(f"   CV: {th_level} | ⭐ Estrelas: {war_stars} | 🏆 Recorde: {best_trophies}")
            print(f"   Heróis: {heroes_str}")

        else:
            print(f"\n-> {player_name}")
            print(f"   !!! Falha ao buscar dados para este jogador.")
        
        time.sleep(0.1) # Pequena pausa para não sobrecarregar a API

    print("\n" + "="*70)
    print("                      RELATÓRIO CONCLUÍDO")
    print("="*70)


if __name__ == "__main__":
    main()