import typing

from ..schema import InputTarget, Target
from ..utils import get_input_target_id


class Targets:
    """Targets methods"""

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
            for target in (await self.request("GET", "targets"))["targets"]
        ]

    async def get_target(self, target: typing.Union[Target, str]) -> Target:
        """
        Get target by ID
        :param target: Target ID
        :return: `Target` object
        :example:
        ```python
            >>> target = await api.targets.get_target(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(target)
            >>> target = await api.targets.get_target(
                    Target(...),
                )
            >>> print(target)
        ```
        """
        return Target.from_dict(
            await self.request("GET", f"targets/{get_input_target_id(target)}")
        )

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
        response: dict = await self.request(
            "POST", "targets/add", {"targets": targets, "groups": groups or []}
        )

        return [
            await self.get_target(target["target_id"]) for target in response["targets"]
        ]

    async def delete_targets(self, targets: typing.List[typing.Union[Target, str]]):
        """
        Delete targets
        :param targets: List of targets
        :return: None
        :example:
        ```python
            >>> await api.targets.delete_targets(
                    [
                        "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                        Target(...),
                    ],
                )
        ```
        """
        await self.request(
            "POST",
            "targets/delete",
            {"targets": [get_input_target_id(target) for target in targets]},
        )

    async def delete_target(self, target: typing.Union[Target, str]):
        """
        Delete target
        :param target: Target
        :return: None
        :example:
        ```python
            >>> await api.targets.delete_target(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.targets.delete_target(
                    Target(...),
                )
        ```
        """
        await self.delete_targets([target])

    async def create_target(
        self,
        target: InputTarget,
        groups: typing.Optional[typing.List[str]] = None,
    ) -> Target:
        """
        Create new target
        :param target: Target
        :param groups: List of groups
        :return: `Target` object
        :example:
        ```python
            >>> target = await api.targets.create_target(
                    InputTarget(
                        address="https://example.com",
                        description="Example",
                    ),
                )
            >>> print(target)
        ```
        """
        return (await self.create_targets([target], groups))[0]
