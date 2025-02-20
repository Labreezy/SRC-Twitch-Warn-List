import argparse, json

import speedruncompy
from speedruncompy import GetGameData, GetGameLeaderboard2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('game_url', type=str.lower)
    return parser.parse_args()

def main():
    args = parse_args()

    game_url = args.game_url
    game_data = GetGameData(gameUrl=game_url).perform()
    gameid = game_data.game.id
    fullgame_categories = [cat for cat in game_data.categories if not cat.isPerLevel]
    platforms = game_data.platforms

    player_id_cache = {}
    for category in fullgame_categories:
        if "Legacy" in category.name:
            continue

        lb = GetGameLeaderboard2(gameId=gameid, categoryId=category.id, verified=speedruncompy.Verified.VERIFIED, obsolete=speedruncompy.ObsoleteFilter.HIDDEN).perform_all()
        newcache = {player.id: player.name for player in lb.playerList}
        player_id_cache.update(newcache)
        twitch_vod_runs = [r for r in lb.runList if r.video is not None and "twitch.tv" in r.video]
        for platform in platforms:
            for r in twitch_vod_runs:
                if r.platformId != platform.id or r.time is None:
                    continue
                runner_name = player_id_cache[r.playerIds[0]]

                print(f"{runner_name} ({category.name}, {platform.name})")

        print("-------")


if __name__ == '__main__':
    main()