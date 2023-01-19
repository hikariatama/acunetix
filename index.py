import asyncio

import acunetix


async def main():
    api = acunetix.AcunetixAPI(
        "1986ad8c0a5b3df4d7028d5f3c06e936cdcc13b0d336841bc93daf7e58fb8a63a",
        "localhost:3443",
    )

    await api.connect()


if __name__ == "__main__":
    asyncio.run(main())
