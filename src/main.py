from os import remove
from argparse import ArgumentParser

from download import download_episodes
from pocketfm import fetch_pocketfm_data, save_data_to_json

RED = "\033[91m"
YELLOW = "\033[93m"
ORANGE = "\033[38;2;253;182;0m"
CYAN = "\033[96m"
RESET = "\033[0m"

def main():
    try:
        parser = ArgumentParser(description="SLD PocketFM Downloader")
        parser.add_argument('url', type=str, nargs='?', help="The URL of the PocketFM show")
        parser.add_argument('-p', '--pattern', type=str, help="The pattern to download episodes\n1. To download all episodes, enter '*'\n2. To download episodes before 'n', enter '*n'\n3. To download episodes after 'n', enter 'n*'\n4. To download episodes between 'n' and 'm', enter 'n*m'\n5. To download a specific episode, enter the episode number.")
        args = parser.parse_args()
        if args.url:
            show_url = args.url
        else:
            show_url = input(f"{CYAN}Enter the show URL: {RESET}")
        show_id = show_url.split("/")[-1]
        stories_data = fetch_pocketfm_data(show_id)
        if stories_data:
            json_filename = f"{show_id}.json"
            save_data_to_json(stories_data, json_filename)
        else:
            print(f"{RED}Failed to fetch data.{RESET}")
            return
        download_pattern = args.pattern
        if not download_pattern:
            print(f'{YELLOW}Enter the pattern to download episodes:{RESET}')
            print(f'{ORANGE} *n -{YELLOW} Download episodes before n{RESET}')
            print(f'{ORANGE} n* -{YELLOW} Download episodes after n{RESET}')
            print(f'{ORANGE} n*m -{YELLOW} Download episodes between n and m{RESET}')
            print(f'{ORANGE} n -{YELLOW} Download a specific episode{RESET}')
            download_pattern = input(f"{CYAN}Pattern: {RESET}")
        download_folder = show_id
        download_episodes(json_filename, download_pattern, download_folder, show_id)
        remove(json_filename)
        print(f"{CYAN}Removed cached files!{RESET}")
    except KeyboardInterrupt:
        print(f"{RED}Exiting...{RESET}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")

if __name__ == "__main__":
    main()
