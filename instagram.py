import instagrapi

import datetime
import logging
import json
import os

try:
    from __main__ import logger
except ImportError:
    logger = logging.getLogger(__name__)



class exceptions:
    class PasswordRequired(Exception):
        pass

class User(instagrapi.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def login(self, username: str, password: str=None, mfaSeed: str=None, mfaCode: str=None, sessionFile: str=None):
        """
        Performs a login operation for the user with the provided credentials.

        Args:
            username (str)
                The username of the user.
            password (str, optional)
                The password of the user. If not provided, it will be prompted from the user.
            mfaSeed (str, optional)
                The multi-factor authentication (MFA) seed of the user. If provided, an MFA code will be prompted from the user.
            mfaCode (str, optional)
                The MFA code of the user. If provided, it will be used for MFA verification.
                However, it is recommended to provide mfaSeed instead of mfaCode.
            sessionFile (str, optional)
                The name of the file where the session will be saved. Will default to "<username>.json".

        Returns:
            None
        """

        
        self.username = username
        self.password = password
        self.sessionFile = f"{self.username}.json" or sessionFile

        self.client = instagrapi.Client()
        try:
            self.client.load_settings(self.sessionFile)
            logger.debug("Session file found, loading...")
        except:
            if self.password is None:
                raise exceptions.PasswordRequired("No session file found, password is required.")
            
            logger.info("No session file found, logging in...")
            if mfaSeed:
                logger.debug("2FA seed provided, generating code...")
                mfaCode = self.client.totp_generate_code(mfaSeed)

        try:
            self.client.login(username, password, verification_code='' if not (mfaSeed or mfaCode) else mfaCode)
            logger.debug("Logged in.")
        except Exception as e:
            if isinstance(e, AttributeError):
                if password is None:
                    logger.exception("Login failed. Password is required.")
                    return
            elif isinstance(e, instagrapi.exceptions.TwoFactorRequired):
                if mfaSeed is None:
                    logger.warning("2FA is enabled, but no seed was provided. For further use, you can provide the seed with the -2fa or --2fa argument.")
                    mfaCode = input("Please enter the 2FA code: ")
                    return self.login(username, password, mfaCode=mfaCode)
            else:
                logger.exception("Login failed.")
                exit()

        logger.info(f"Successfully logged in as {self.client.account_info().username}!")

        self.client.dump_settings(self.sessionFile)
        logger.debug("Session file saved.")


    def getFollowers(self):
        """
        Fetch the followers of the user.
        """
        logger.debug("Fetching followers...")
        
        _followers = self.client.user_followers(self.client.user_id)
        followers = []
        for followerId in _followers:
            follower = _followers[followerId].dict()
            del follower['stories']

            followers.append( follower )

        logger.debug("Fetched followers.")
        return followers

    def exportFollowers(self):
        """
        Exports the followers of the user to a JSON file.
        """
        followers = self.getFollowers()

        date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

        if not os.path.exists(f"followers-{self.username}"):
            os.mkdir(f"followers-{self.username}")

        with open(f"followers-{self.username}/{date}.json", "w", encoding='utf-8') as f:
            json.dump(followers, f, indent=2, ensure_ascii=False)

        logger.info(f"Successfully exported {len(followers)} followers to followers-{self.username}/{date}.json")


    def getFollowing(self):
        """
        Fetch the following of the user.
        """
        logger.debug("Fetching following...")

        _following = self.client.user_following(self.client.user_id)
        following = []
        for followingId in _following:
            followingUser = _following[followingId].dict()
            del followingUser['stories']

            following.append( followingUser )

        logger.debug("Fetched following.")
        return following

    def exportFollowing(self):
        """
        Exports the following of the user to a JSON file.
        """
        following = self.getFollowing()

        date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

        if not os.path.exists(f"following-{self.username}"):
            os.mkdir(f"following-{self.username}")

        with open(f"following-{self.username}/{date}.json", "w", encoding='utf-8') as f:
            json.dump(following, f, indent=2, ensure_ascii=False)

        logger.info(f"Successfully exported {len(following)} following to following-{self.username}/{date}.json")


    def compareFollowersAndFollowing(self, returnRaw=False):
        """
        Compares the followers and following of the user.
        """
        followers = self.getFollowers()
        following = self.getFollowing()

        followerIds = [u['pk'] for u in followers]
        followingIds = [u['pk'] for u in following]

        notFollowedBack = []
        notFollowingBack = []
        
        for user in followerIds:
            if user in followingIds:
                continue
            notFollowingBack.append(user)

        for user in followingIds:
            if user in followerIds:
                continue
            notFollowedBack.append(user)

        logger.debug("%i users are not following back" % len(notFollowedBack))
        logger.debug("You don't follow back %i users" % len(notFollowingBack))
        
        logger.debug("Obtaining users informations...")
        data = {
            "notFollowedBack": [
                self.client.user_info(userId).dict() for userId in notFollowedBack
            ],
            "notFollowingBack": [
                self.client.user_info(userId).dict() for userId in notFollowingBack
            ]
        }
        logger.debug("Obtained users informations.")
        if returnRaw:
            return data
        
        import functions
        return functions.followeeComparison(
            self.client.username,
            followers, following,
            data
        )
