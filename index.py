import requests
from collections import defaultdict

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdlOTExMGNmLWE0ZGYtNDk5Ni1iZjAzLTNlM2RkMDI0NWY0ZCIsImlhdCI6MTc1NDE3Njk4OCwic3ViIjoiZGV2ZWxvcGVyL2ViOTczZmIwLTEwYjQtMjM5Yi0zNWZjLTFlODQ0MDc4ZWYwYSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE4OS4yNy4xNzIuNzYiXSwidHlwZSI6ImNsaWVudCJ9XX0.nuXJE2mdc5TrBX9L-TclJT4tDmcnyxNp4JTW4Mo2wjoOoNz3CV7L8xmxqljxX1AyTn7cxASLI3cJg9usDIj9Bg"

CLAN_TAG = "#2G9CPRO90"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def url_encode_tag(tag):
    return tag.replace('#', '%23')

def get_war_log(clan_tag):
    url = f"https://api.clashofclans.com/v1/clans/{url_encode_tag(clan_tag)}/warlog"
    response = requests.get(url, headers=HEADERS)
    print("Status code:", response.status_code)
    print("Response text (resumido):", response.text[:500])  # imprime os primeiros 500 caracteres para não lotar
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar histórico de guerras: {response.status_code} - {response.text}")
        return None

def analyze_players_in_warlog(war_log):
    player_stats = defaultdict(lambda: {
        'name': '',
        'attacks': 0,
        'stars': 0,
        'destruction': 0.0
    })

    items = war_log.get('items', [])
    print(f"Quantidade de guerras no histórico: {len(items)}")  # Debug

    for war in items:
        if 'members' not in war:
            print("Aviso: Guerra sem membros (pode ser guerra amigável ou outro tipo). Ignorando.")
            continue
        for member in war.get('members', []):
            tag = member['tag']
            name = member.get('name', 'Unknown')
            attacks = member.get('attacks', [])

            stats = player_stats[tag]
            stats['name'] = name
            stats['attacks'] += len(attacks)
            stats['stars'] += sum(a['stars'] for a in attacks)
            stats['destruction'] += sum(a['destructionPercentage'] for a in attacks)

    # Calcular médias
    for tag, stats in player_stats.items():
        if stats['attacks'] > 0:
            stats['avg_stars'] = stats['stars'] / stats['attacks']
            stats['avg_destruction'] = stats['destruction'] / stats['attacks']
        else:
            stats['avg_stars'] = 0
            stats['avg_destruction'] = 0.0

    return player_stats

def rank_players(player_stats):
    return sorted(player_stats.items(), key=lambda x: (x[1]['avg_stars'], x[1]['avg_destruction']), reverse=True)

def main():
    war_log = get_war_log(CLAN_TAG)
    if not war_log:
        print("Não foi possível obter histórico de guerras.")
        return

    player_stats = analyze_players_in_warlog(war_log)
    if not player_stats:
        print("Nenhum dado de jogador encontrado no histórico de guerras.")
        return

    ranked = rank_players(player_stats)

    print("Ranking de jogadores pelo desempenho no histórico de guerras:\n")
    for idx, (tag, stats) in enumerate(ranked, 1):
        print(f"{idx}. {stats['name']} (Tag: {tag})")
        print(f"   Ataques: {stats['attacks']}, Estrelas totais: {stats['stars']}")
        print(f"   Média de estrelas por ataque: {stats['avg_stars']:.2f}")
        print(f"   Média de destruição por ataque: {stats['avg_destruction']:.2f}%\n")

if __name__ == "__main__":
    main()