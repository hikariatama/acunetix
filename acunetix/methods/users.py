import hashlib
import typing

from ..schema import User
from ..utils import get_input_user_id


class Users:
    """Users methods"""

    async def get_users(self) -> typing.List[User]:
        """
        Get all users
        :return: List of `User` objects
        :example:
        ```python
            >>> users = await api.users.get_users()
            >>> for user in users:
            >>>     print(user)
        ```
        """
        return [
            User.from_dict(user)
            for user in (await self.request("GET", "users"))["users"]
        ]

    async def get_user(self, user: typing.Union[User, str]) -> User:
        """
        Get user by ID
        :param user_id: User ID or `User` object
        :return: `User` object
        :example:
        ```python
            >>> user = await api.users.get_user(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(user)
        ```
        """
        return User.from_dict(
            await self.request("GET", f"users/{get_input_user_id(user)}")
        )

    async def create_user(
        self,
        first_name: str,
        last_name: str,
        role: str,
        email: str,
        password: str,
    ) -> User:
        """
        Create new user
        :param username: Username
        :param password: Password
        :param email: Email
        :param role: Role
        :return: `User` object
        :example:
        ```python
            >>> user = await api.users.create_user(
                    "John",
                    "Doe",
                    "platform_admin",
                    "login@example.com",
                    "p@55w0rd",
                )
            >>> print(user)
        ```
        """
        return User.from_dict(
            await self.request(
                "POST",
                "users",
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "email": email,
                    "password": hashlib.sha256(password.encode()).hexdigest(),
                },
            )
        )

    async def disable_users(
        self,
        users_list: typing.List[typing.Union[User, str]],
    ) -> None:
        """
        Disable users by IDs
        :param users_list: User ID list or `User` object list
        :return: None
        :example:
        ```python
            >>> await api.users.disable_users(
                    [
                        "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                        User(...),
                    ],
                )
        ```
        """
        await self.request(
            "POST",
            "users/disable",
            json={"user_id_list": [get_input_user_id(user) for user in users_list]},
        )

    async def enable_users(
        self,
        users_list: typing.List[typing.Union[User, str]],
    ) -> None:
        """
        Enable users by IDs
        :param users_list: User ID list or `User` object list
        :return: None
        :example:
        ```python
            >>> await api.users.enable_users(
                    [
                        "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                        User(...),
                    ],
                )
        ```
        """
        await self.request(
            "POST",
            "users/enable",
            json={"user_id_list": [get_input_user_id(user) for user in users_list]},
        )

    async def delete_users(
        self,
        users_list: typing.List[typing.Union[User, str]],
    ) -> None:
        """
        Delete users by IDs
        :param users_list: User ID list or `User` object list
        :return: None
        :example:
        ```python
            >>> await api.users.delete_users(
                    [
                        "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                        User(...),
                    ],
                )
        ```
        """
        await self.request(
            "POST",
            "users/delete",
            json={"user_id_list": [get_input_user_id(user) for user in users_list]},
        )

    async def disable_user(self, user: typing.Union[User, str]) -> None:
        """
        Disable user by ID
        :param user_id: User ID
        :return: None
        :example:
        ```python
            >>> await api.users.disable_user(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.users.disable_user(User(...))
        ```
        """
        return await self.disable_users([user])

    async def enable_user(self, user: typing.Union[User, str]) -> None:
        """
        Enable user by ID
        :param user_id: User ID
        :return: None
        :example:
        ```python
            >>> await api.users.enable_user(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.users.enable_user(User(...))
        ```
        """
        return await self.enable_users([user])

    async def delete_user(self, user: typing.Union[User, str]) -> None:
        """
        Delete user by ID
        :param user_id: User ID
        :return: None
        :example:
        ```python
            >>> await api.users.delete_user(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.users.delete_user(User(...))
        ```
        """
        return await self.delete_users([user])

    async def update_user(
        self,
        user: typing.Union[User, str],
        first_name: str,
        last_name: str,
        role: str,
        email: str,
    ) -> User:
        """
        Update user
        :param user: User ID or `User` object
        :param username: Username
        :param email: Email
        :param role: Role
        :return: `User` object
        :example:
        ```python
            >>> user = await api.users.update_user(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                    "John",
                    "Doe",
                    "platform_admin",
                    "login@example.com",
                )
            >>> print(user)
        ```
        """

        await self.request(
            "PATCH",
            f"users/{get_input_user_id(user)}",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "email": email,
            },
        )

        return await self.get_user(user)
