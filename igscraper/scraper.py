#!/usr/bin/env python3.8

from instagram_private_api import Client, errors
from yaspin import yaspin, Spinner
from datetime import datetime

import re


class IGScraper(object):
    def __init__(self, username: str, password: str):

        self.spinner = Spinner(["[ ]", "[.]", "[:]", "[.]", "[ ]"], 200)

        with yaspin(self.spinner, text="login") as spinner:
            try:
                self.client = Client(username=username, password=password)
                spinner.text = "login success"
                spinner.ok("[+]")

            except errors.ClientLoginError as error:
                spinner.text = "login error invalid username or password"
                spinner.fail("[-]")
                raise errors.ClientLoginError(error)

    def __get_user_info(self, username: str) -> dict:
        """Returns all user information"""

        with yaspin(self.spinner, text="get user information") as spinner:
            try:
                user_info = self.client.username_info(username)
                spinner.ok("[+]")

            except errors.ClientError as error:
                spinner.text = f"user not found: {username}"
                spinner.fail("[-]")
                raise errors.ClientError(error)

        return user_info

    def __get_hd_profile_pic(self, user_info: dict) -> str:
        """Returns the URL to the profile image"""

        hd_profile_pic_url_info = user_info.get("user", {}).get(
            "hd_profile_pic_url_info", {}
        )
        return hd_profile_pic_url_info.get("url", "None")

    def __get_phone_numbers(self, user_info: dict) -> list:
        """Gets the phone numbers of the user"""

        phone_numbers = list()
        if user_info.get("user", {}).get("contact_phone_number"):
            phone_numbers.append(user_info["user"]["contact_phone_number"])

        user_bio = user_info.get("user", {}).get("biography", "")
        phone_number = re.findall(
            r"\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{6})", user_bio
        )

        if phone_number:
            phone_numbers.append("".join(phone_number[0]))

        return phone_numbers

    def __get_emails(self, user_info: dict) -> list:
        """Gets the emails of the user"""

        emails = list()
        if user_info.get("user", {}).get("public_email"):
            emails.append(user_info["user"]["public_email"])

        user_bio = user_info.get("user", {}).get("biography", "")
        user_email = re.findall(
            r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+", user_bio
        )
        if user_email:
            emails.append(user_email[0])

        return emails

    def __get_username_feed(self, username: str, media_count: int) -> list:
        """Returns the information of all posts"""

        user_feed = list()
        if not media_count:
            return user_feed

        try:
            result = self.client.username_feed(username)

        except errors.ClientError as identifier:
            raise identifier

        user_feed.extend(result.get("items", []))
        next_max_id = result.get("next_max_id")
        while next_max_id:
            result = self.client.username_feed(username, max_id=next_max_id)
            user_feed.extend(result.get("items", []))
            if len(user_feed) >= media_count:
                break
            else:
                next_max_id = result.get("next_max_id")

        return user_feed

    def __get_likes_count(self, user_feed: list) -> int:
        """The sum of all the likes in the publications is obtained"""

        return sum(item.get("like_count", 0) for item in user_feed)

    def __get_comment_count(self, user_feed: list) -> int:
        """The sum of all the comments in the publications is obtained"""

        return sum(item.get("comment_count", 0) for item in user_feed)

    def __get_frequency_posts(self, user_feed: list) -> str:
        """Gets the frequency in days which it's published"""

        dates = [datetime.fromtimestamp(item.get("taken_at", 0)) for item in user_feed]
        dates.reverse()
        diffs = list()
        for index, item in enumerate(dates):
            try:
                diff = dates[index + 1] - item
                diffs.append(diff.days)

            except Exception:
                diff = datetime.now() - item
                diffs.append(diff.days)

        return "None" if not diffs else f"{round(sum(diffs) / len(diffs))} days"

    def __get_posts(self, user_feed: list) -> dict:
        """Get information of the all posts"""

        posts = dict()
        for index, item in enumerate(user_feed, start=1):

            posts[index] = {
                "date": str(datetime.fromtimestamp(item.get("taken_at", ""))),
                "url": f"https://instagram.com/p/{item.get('code', 'None')}/",
                "comment_count": item.get("comment_count", "None"),
                "like_count": item.get("like_count", "None"),
                "text": item.get("caption", {}).get("text", "None"),
            }

            if item.get("location"):
                location = item["location"]
                posts[index].update(
                    {
                        "location": {
                            "name": location.get("name", "None"),
                            "lng": location.get("lng", "None"),
                            "lat": location.get("lat", "None"),
                        }
                    }
                )

        return posts

    def username_info(self, username: str) -> dict:

        user_info = self.__get_user_info(username)
        hd_profile_pic = self.__get_hd_profile_pic(user_info)
        user_phones = self.__get_phone_numbers(user_info)
        user_emails = self.__get_emails(user_info)
        media_count = user_info.get("user", {}).get("media_count", 0)
        user_feed = self.__get_username_feed(username, media_count)
        followers = user_info.get("user", {}).get("follower_count", "None")
        likes_count = self.__get_likes_count(user_feed)
        comment_count = self.__get_comment_count(user_feed)
        engagement_rate = round((likes_count + comment_count) / followers * 100)
        frequency_posts = self.__get_frequency_posts(user_feed)
        posts = self.__get_posts(user_feed)

        return {
            "username": username,
            "name": user_info.get("user", {}).get("full_name", "None"),
            "followers": followers,
            "following": user_info.get("user", {}).get("following_count", "None"),
            "media_count": media_count,
            "biography": user_info.get("user", {}).get("biography", "None"),
            "hd_profile_pic": hd_profile_pic,
            "website": user_info.get("user", {}).get("external_url", "None"),
            "likes_count": likes_count,
            "comment_count": comment_count,
            "engagement_rate": engagement_rate,
            "frequency_posts": frequency_posts,
            "phone_numbers": user_phones,
            "emails": user_emails,
            "is_bussines": user_info.get("is_bussines", "None"),
            "is_verified": user_info.get("is_verified", "None"),
            "is_private": user_info.get("is_private", "False"),
            "posts": posts,
        }
