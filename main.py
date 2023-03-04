import os
import dotenv
import argparse
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('FolloRizz')

import instagram
igClient = instagram.User()

import menu
import inputs


def displayBanner():
    print("  ___ ___  _    _    ___  ___ ___ ________")
    print(" | __/ _ \| |  | |  / _ \| _ \_ _|_  /_  /")
    print(" | _| (_) | |__| |_| (_) |   /| | / / / / ")
    print(" |_| \___/|____|____\___/|_|_\___/___/___|")
    print("                                          ")
    print("         Made with <3 by @gahrlt          ")
    print("                                          ")

def clearScreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def app(parsedArgs):
    #~ Initialize Instagram user
    if parsedArgs.env:
        env = {
            **os.environ,
            **dotenv.dotenv_values('.env'),
            **dotenv.dotenv_values(parsedArgs.env)
        }
        igClient.login(
            env['INSTAGRAM_USERNAME'], env['INSTAGRAM_PASSWORD'],
            mfaSeed=env['INSTAGRAM_2FA_SEED'], sessionFile=f'{env.get("SESSION_FILE_PATH")}.json'
        )
    else:
        igClient.login(
            parsedArgs.username, parsedArgs.password,
            mfaSeed=parsedArgs.twofseed, sessionFile=f'{parsedArgs.username}.json'
        )

    #~ Display menu
    displayBanner()
    print(f'Welcome @{igClient.username}! Here is the menu:')
    nbOpts = menu.Home.display()
    _, choice = print('What do you want to do?', end=' '), inputs.getInteger(1, nbOpts)

    clearScreen()
    displayBanner()
    menu.Home.opts[choice - 1]['action']()

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="FolloRizz",
        description='Utility tool to play with your Instagram account followers/following lists',
        epilog='Made with <3 by @gahrlt'
    )
    #~ Only provide either username or env file
    dataGroup = parser.add_mutually_exclusive_group(required=True)
    dataGroup.add_argument('--username', '-u', help='Instagram username')
    dataGroup.add_argument('--env', help='Environment file where credentials are stored')
    
    parser.add_argument('--password', '-p', help='Instagram password', required=False)
    parser.add_argument('--twofseed', '-2fa', '--2fa', '-mfa', '--mfa', help='2FA seed', required=False)
    
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    app(args)