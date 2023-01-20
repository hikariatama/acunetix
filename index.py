import asyncio
import os
import acunetix


async def main():
    api = acunetix.AcunetixAPI(
        "1986ad8c0a5b3df4d7028d5f3c06e936cdcc13b0d336841bc93daf7e58fb8a63a",
        "localhost:3443",
    )

    await api.connect()

    files = await api.default_scan(
        acunetix.schema.input_target.InputTarget("https://hikariatama.ru/hikka"),
        acunetix.schema.scan_profile.CRAWL_ONLY,
    )

    for file in files:
        with open(os.path.join("reports", file.name), "wb") as f:
            f.write(file.read())

    print("Successfully downloaded reports:")
    print(os.listdir("reports"))


if __name__ == "__main__":
    asyncio.run(main())
