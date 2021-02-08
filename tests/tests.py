#!/usr/bin/env python3.8

from instagram_private_api import errors
from pathlib import Path
from sys import path

path.insert(0, str(Path(__file__).resolve().parents[1]))
from igscraper.scraper import IGScraper

import unittest
import yaml


def get_credentials():

    with open("config.yml", "r") as yml:
        credentials = yaml.load(yml, Loader=yaml.FullLoader)

    return credentials["user"], credentials["password"]


class TestIGScraper(unittest.TestCase):

    invalid_username = "u#$%mgwsekqhumgiwkqh"
    random_password = "97801471349780147134"
    valid_username = "_jxlil"

    def test_login(self):

        with self.assertRaises(errors.ClientLoginError):
            IGScraper(self.invalid_username, self.random_password)
            IGScraper(self.valid_username, self.random_password)

    def test_get_userinfo(self):

        try:
            user, password = get_credentials()
            scraper = IGScraper(user, password)

        except errors.ClientLoginError as error:
            print("[!] a valid username and password are required to perform this test")
            raise errors.ClientLoginError(error)

        # invalid username
        with self.assertRaises(errors.ClientError):
            scraper._IGScraper__get_user_info(self.invalid_username)

        # valid username
        userinfo = scraper._IGScraper__get_user_info(self.valid_username)
        self.assertTrue(userinfo.get("user"))


if __name__ == "__main__":
    unittest.main()
