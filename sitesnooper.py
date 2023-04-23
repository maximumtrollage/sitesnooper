#!/usr/bin/env python3

import argparse
import urllib.parse
from pathlib import Path

import colorama
import requests
from colorama import Fore, Style
from tqdm import tqdm

colorama.init(autoreset=True)


def getArgs() -> tuple[str, str]:
    """Just get's the arguments from the command line, ez.

    Returns:
        tuple[str, str]: 0-index is the site, 1-index is the wordlist path.
    """
    parser = argparse.ArgumentParser(
        description="SiteSnooper is basically a simplified dirbuster."
    )
    parser.add_argument(
        "-s", "--site", dest="site", help="pass in the site URL", required=True
    )
    parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        help="connection timeout in seconds",
        required=True,
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        dest="wordlist",
        help="pass in the path to a wordlist",
        required=True,
    )

    args = parser.parse_args()
    site = args.site
    timeout = args.timeout
    wordlist = args.wordlist

    return (site, timeout, wordlist)


def deUrl(site):
    site = turnToUrl(site)
    site = urllib.parse.urlparse(site)
    domain_components = site.netloc.split(":")[0].split(".")

    if len(domain_components) < 2:
        raise ValueError("Invalid domain name")

    domain_name = domain_components[-2]
    return domain_name


def turnToUrl(site: str) -> str:
    if "http://" not in site and "https://" not in site:
        site = f"http://{site}"

    urllib.parse.quote(site)
    return site


def checkIfSiteUp(site: str, timeout) -> tuple[bool, str]:
    site = turnToUrl(site)
    try:
        resp = requests.get(site, timeout=float(timeout))
        if resp.ok:
            return (True, "Site is up.")
        else:
            return (False, f"Error: {resp.status_code}")
    except requests.exceptions.Timeout:
        return (False, "Connection timed out.")
    except requests.exceptions.ConnectionError:
        return (False, f'Failed to connect to "{site}".')
    except requests.exceptions.RequestException as ex:
        return (False, f"Something went wrong! ({str(ex)}).")
    except ValueError:
        return (False, f"Timeout must be an int/float, not {type(timeout).__name__}")


def checkIfFileExists(file_path: str) -> bool:
    file = Path(file_path)
    if file.is_file():
        return True

    return False


def getSitePath(site: str, timeout) -> tuple[bool, str]:
    site = turnToUrl(site)
    try:
        resp = requests.get(site, timeout=float(timeout))
        if resp.ok:
            return (True, resp.content)
        else:
            return (False, f"Error: {resp.status_code}")
    except requests.exceptions.Timeout:
        return (False, "Connection timed out.")
    except requests.exceptions.ConnectionError:
        return (False, f'Failed to connect to "{site}".')
    except requests.exceptions.RequestException as ex:
        return (False, f"Something went wrong! ({str(ex)}).")
    except ValueError:
        return (False, f"Timeout must be an int/float, not {type(timeout).__name__}")


def check_wordlist(site: str, wordlist_path: str, timeout):
    site = turnToUrl(site)
    toFile(f"./{deUrl(site)}/exists.txt", "")
    toFile(f"./{deUrl(site)}/doesnt_exist.txt", "")
    with open(wordlist_path) as f:
        wordlist = [line.strip() for line in f if line.strip()]
        with tqdm(total=len(wordlist), bar_format="{desc}: {percentage:3.0f}%|{bar:100}{r_bar}", leave=False) as pbar:
            for line in wordlist:
                line = f"{site}/{line}"

                (success, content) = getSitePath(line, timeout=timeout)

                if success:
                    toFile(f"./{deUrl(site)}/exists.txt", f"{line}\n", True)
                    pbar.write(f"    {Fore.GREEN}exists: {Style.BRIGHT}{Fore.BLACK}{line}")
                else:
                    toFile(f"./{deUrl(site)}/doesnt_exist.txt", f"{line}\n", True)

                pbar.update(1)


def toFile(path, what, append: bool = False):
    file_path = Path(path)
    parent_dir = file_path.parent
    if not append:
        parent_dir.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            with file_path.open("w+") as f:
                f.write(what)
        else:
            with file_path.open("w") as f:
                f.write(what)
        return

    parent_dir.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        with file_path.open("a+") as f:
            f.write(what)
    else:
        with file_path.open("a") as f:
            f.write(what)


def printTitle():
    print(
        f"""{Fore.CYAN}{Style.BRIGHT}
   _____ _ _        _____                                   
  / ____(_) |      / ____|                                  
 | (___  _| |_ ___| (___  _ __   ___   ___  _ __   ___ _ __ 
  \___ \| | __/ _ \\\___ \| '_ \ / _ \ / _ \| '_ \ / _ \ '__|
  ____) | | ||  __/____) | | | | (_) | (_) | |_) |  __/ |   
 |_____/|_|\__\___|_____/|_| |_|\___/ \___/| .__/ \___|_|   
    made by: maximumtrollage               | |              
       "h" (79735) on VACBAN               |_|              \n"""
    )


"""
- #abb2bf  Style.DIM     (light gray)
- #56b6c2  Fore.CYAN     (cyan)
- #61afef  Fore.BLUE     (blue)
- #98c379  Fore.GREEN    (green)
- #e06c75  Fore.RED      (red)
- #c678dd  Fore.MAGENTA  (purple)
"""


def main():
    printTitle()

    site, timeout, wordlist = getArgs()

    print(
        f"""    {Style.BRIGHT}Site....: {Fore.BLACK}{turnToUrl(site)}{Fore.WHITE}
    Timeout.: {Fore.BLACK}{timeout}{Fore.WHITE}
    Wordlist: {Fore.BLACK}{wordlist}
"""
    )

    isSiteUp = checkIfSiteUp(site, timeout)

    if not isSiteUp[0]:
        print(f"{Fore.RED}{isSiteUp[1]}")
        return

    if not checkIfFileExists(wordlist):
        print(f"{Fore.RED}The wordlist path does not exist!")
        return

    toFile(
        f"./{deUrl(site)}/README.txt",
        """
   _____ _ _        _____                                   
  / ____(_) |      / ____|                                  
 | (___  _| |_ ___| (___  _ __   ___   ___  _ __   ___ _ __ 
  \___ \| | __/ _ \\\___ \| '_ \ / _ \ / _ \| '_ \ / _ \ '__|
  ____) | | ||  __/____) | | | | (_) | (_) | |_) |  __/ |   
 |_____/|_|\__\___|_____/|_| |_|\___/ \___/| .__/ \___|_|   
    made by: maximumtrollage               | |              
       "h" (79735) on VACBAN               |_|               \n\n""",
    )
    toFile(
        f"./{deUrl(site)}/README.txt",
        f"""    Site....: {turnToUrl(site)}
    Timeout.: {timeout}
    Wordlist: {wordlist}\n\n./exists.txt contains paths that, well, exist.\nThe opposite for ./doesnt_exist.txt\n\n\nWhat was/wasn't found?\n""",
        True,
    )

    robotsTxtExist = getSitePath(f"{site}/robots.txt", timeout=timeout)
    if robotsTxtExist[0]:
        toFile(f"./{deUrl(site)}/README.txt", "     was: /robots.txt\n", True)
        lines = robotsTxtExist[1].decode("utf-8").splitlines()
        lines = len(lines)
        if lines > 10:
            print(
                f"{Fore.YELLOW}/robots.txt is too big! output located at ./{deUrl(site)}/robots.txt"
            )
            toFile(f"./{deUrl(site)}/robots.txt", robotsTxtExist[1].decode("utf-8"))
        else:
            toFile(f"./{deUrl(site)}/robots.txt", robotsTxtExist[1].decode("utf-8"))
            print(f"/robots.txt:\n{robotsTxtExist[1].decode('utf-8')}")

        if "Sitemap" in robotsTxtExist[1].decode(
            "utf-8"
        ) or "sitemap" in robotsTxtExist[1].decode("utf-8"):
            print(f'{Fore.GREEN}Found "sitemap" in /robots.txt:')
            toFile(f"./{deUrl(site)}/sitemap.txt", "")
            toFile(f"./{deUrl(site)}/README.txt", "     was: /sitemap.txt\n", True)
            lines = robotsTxtExist[1].decode("utf-8").splitlines()
            for line in lines:
                if "Sitemap" in line or "sitemap" in line:
                    toFile(f"./{deUrl(site)}/sitemap.txt", f"{line}\n", True)
                    print(f"{Fore.BLACK}{Style.BRIGHT}    {line}")
        else:
            toFile(f"./{deUrl(site)}/README.txt", "     wasn't: sitemap\n", True)
            print(f'{Fore.YELLOW}"Sitemap" wasn\'t found in /robots.txt')
    else:
        toFile(f"./{deUrl(site)}/README.txt", "     wasn't: /robotx.txt\n", True)
        print(f"{site} does not have a robots.txt!")

    print(f"{Style.BRIGHT}Checking wordlist: {wordlist}")
    check_wordlist(site, wordlist, timeout=timeout)
    print(f"\n{Style.BRIGHT}Done.")
    print(f"{Fore.CYAN}Everything was logged to: ./{deUrl(site)}")


if __name__ == "__main__":
    main()
