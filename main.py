import os
import re
import sys
import requests

from bs4 import BeautifulSoup

def get_episode_info(program_title, program_subtitle):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=1',
        'TE': 'trailers',
    }

    res = requests.get('https://northboot.xyz/search?q=%21ddg+site%3Afernsehserien.de+' + program_title + ' ' + program_subtitle, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    for i, result in enumerate(soup.find_all('article')):
        if i >= 8:
            return None
        result_url = result.find('a').get('href')
        match = re.search(r'\/folgen\/(\d{1,2})x(\d{1,2})-', result_url)
        if match:
            season_number = match.group(1)
            episode_number = match.group(2)
            return f"{program_title} S{season_number.zfill(2)}E{episode_number.zfill(2)}"
    return None

def move_file(program_title, episode_info, file_path, output_path):
    if episode_info:
        match = re.match(program_title + r" S(\d{2})E(\d{2})", episode_info)
        if match:
            season_number = match.group(1)
            episode_number = match.group(2)

            target_directory = os.path.join(output_path, program_title, "Season " + season_number)
            os.makedirs(target_directory, exist_ok=True)

            target_path = os.path.join(target_directory, f"{program_title} S{season_number}E{episode_number}.ts")
            os.rename(file_path, target_path)
            print(f"The file was successfully moved to: {target_path}")
        else:
            print("Error: Episode information could not be extracted.")
    else:
        print("Error: No episode information found.")




if __name__ == "__main__":

    program_title = sys.argv[1]
    program_subtitle = sys.argv[2]
    file_path = sys.argv[3]
    output_path = sys.argv[4]

    episode_info = get_episode_info(program_title, program_subtitle)
    
    move_file(program_title, episode_info, file_path, output_path)


# python main.py "%t" "%u" "%f" NEWPATH