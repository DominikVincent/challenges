from isi_bot.game_watcher.game_watcher import get_spielberichte_url, get_spielberichte_content

OFFLINE = True

def main():
    spielberichte_urls = get_spielberichte_url(OFFLINE)

    content = get_spielberichte_content(spielberichte_urls)
    print(content)

    
if __name__ == "__main__":
    main()