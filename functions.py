import menu
import inputs

import os
import json
import logging
import datetime

try:
    from __main__ import logger
except ImportError:
    logger = logging.getLogger(__name__)


def followeeComparison(username: str, followers, following, data: dict):
        print("You are following %i users, and %i users are following you." % (len(following), len(followers)))
        print("%i users are not following back" % len(data['notFollowedBack']))
        print("You don't follow back %i users" % len(data['notFollowingBack']))

        nbOpts = menu.FolloweeComparison.display()
        _, choice = print('What do you want to do?', end=' '), inputs.getInteger(1, nbOpts)
        choice = menu.FolloweeComparison.opts[choice - 1]['value']

        if choice == 'export_followers_you_dont_follow':
            key = 'notFollowingBack'

        elif choice == 'export_followers_who_dont_follow_you':
            key = 'notFollowedBack'

        elif choice == 'export_all':
            key = '*'
        

        date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

        if key == '*':
            for key in data:
                if not os.path.exists(f"{key}-{username}"):
                    os.mkdir(f"{key}-{username}")

                with open(f"{key}-{username}/{date}.json", "w", encoding='utf-8') as f:
                    json.dump(data[key], f, indent=2, ensure_ascii=False)

                logger.info(f"Successfully exported {len(data[key])} followers to {key}-{username}/{date}.json")
        else:

            if not os.path.exists(f"{key}-{username}"):
                os.mkdir(f"{key}-{username}")

            with open(f"{key}-{username}/{date}.json", "w", encoding='utf-8') as f:
                json.dump(data[key], f, indent=2, ensure_ascii=False)

            logger.info(f"Successfully exported {len(data[key])} users to {key}-{username}/{date}.json")

