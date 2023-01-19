import typing

from ..schema import InputTarget, Target


class Targets:
    async def get_targets(self) -> typing.List[Target]:
        """
        Get all targets
        :return: List of `Target` objects
        :example:
        ```python
            >>> targets = await api.targets.get_targets()
            >>> for target in targets:
            >>>     print(target)
        ```
        """
        return [
            Target.from_dict(target)
            for target in (await self._request("GET", "targets"))["targets"]
        ]

    async def get_target(self, target_id: str) -> Target:
        """
        Get target by ID
        :param target_id: Target ID
        :return: `Target` object
        :example:
        ```python
            >>> target = await api.targets.get_target(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(target)
        ```
        """
        return Target.from_dict(await self._request("GET", f"targets/{target_id}"))

    async def create_targets(
        self,
        targets: typing.List[InputTarget],
        groups: typing.Optional[typing.List[str]] = None,
    ) -> Target:
        """
        Create new targets
        :param targets: List of targets
        :param groups: List of groups
        :return: List of `Target` objects
        :example:
        ```python
            >>> targets = await api.targets.create_targets(
                    [
                        InputTarget(
                            address="https://example.com",
                            description="Example",
                        ),
                        InputTarget(
                            address="https://example.org",
                            description="Example",
                        ),
                    ],
                )
            >>> for target in targets:
            >>>     print(target)
        ```
        """
        data = {"targets": targets, "groups": groups or []}
        response = await self._request("POST", "targets/add", data)

        return [
            await self.get_target(target["target_id"]) for target in response["targets"]
        ]
