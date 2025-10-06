import requests
from collections import defaultdict

# SEU TOKEN - NÃO PRECISA MUDAR
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJjMGZhMDZmLWExNDYtNDk0OC05OTdiLTE1Y2M5ZTRjMGIwYiIsImlhdCI6MTc1OTc4MTI1OSwic3ViIjoiZGV2ZWxvcGVyL2ViOTczZmIwLTEwYjQtMjM5Yi0zNWZjLTFlODQ0MDc4ZWYwYSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS4yMjIuMjM4LjE1NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.PWK_oSiYMXEs0WLzOx5Ju2BeaORpuSePI4v0seYuCyoMsyFaHeLiViPoHb41trpB6oSdbN3B3344jYmJktFKSQ"

CLAN_TAG = "#2G9CPRO90"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def url_encode_tag(tag):
    """Converte a tag # a para o formato de URL."""
    return tag.replace('#', '%23')

def get_clan_info(clan_tag):
    """Busca informações detalhadas de um clã, incluindo a lista de membros."""
    url = f"https://api.clashofclans.com/v1/clans/{url_encode_tag(clan_tag)}"
    print(f">>> Buscando informações do clã {clan_tag}...")
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        print(">>> Informações recebidas com sucesso!")
        return response.json()
    else:
        print(f"!!! Erro ao buscar informações do clã: {response.status_code} - {response.text}")
        return None

def main():
    clan_data = get_clan_info(CLAN_TAG)
    
    if not clan_data:
        return

    clan_name = clan_data.get('name', 'N/A')
    total_members = clan_data.get('members', 0)
    
    print("\n" + "="*50)
    print(f"RELATÓRIO DO CLÃ: {clan_name}")
    print(f"Total de Membros: {total_members}")
    print("="*50 + "\n")

    member_list = clan_data.get('memberList', [])

    if not member_list:
        print("Nenhum membro encontrado.")
        return

    # Organiza a lista de membros por cargo (Líder primeiro, etc.)
    role_order = {'leader': 0, 'coLeader': 1, 'admin': 2, 'member': 3}
    sorted_members = sorted(member_list, key=lambda m: role_order.get(m.get('role', 'member'), 4))

    for member in sorted_members:
        name = member.get('name', 'N/A')
        tag = member.get('tag', 'N/A')
        role = member.get('role', 'N/A').replace('admin', 'Ancião').replace('coLeader', 'Co-líder').replace('leader', 'Líder').replace('member', 'Membro')
        exp_level = member.get('expLevel', 0)
        trophies = member.get('trophies', 0)
        league = member.get('league', {}).get('name', 'Sem Liga')
        donations = member.get('donations', 0)
        donations_received = member.get('donationsReceived', 0)

        print(f"-> {name} (Tag: {tag})")
        print(f"   Cargo: {role} | Nível: {exp_level}")
        print(f"   Liga: {league} | Troféus: {trophies}")
        print(f"   Tropas Doadas: {donations} | Recebidas: {donations_received}\n")

if __name__ == "__main__":
    main()