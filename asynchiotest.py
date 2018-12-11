from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math
import asyncio
import random


async def task(name):
    r = random.randrange(10)
    await asyncio.sleep(r*10)
    print(name)
    return (name, r)


async def main():
    tasks = []
    for i in range(20):
        tasks.append(
            asyncio.create_task(task(f'Task {i}'))
        )

    ress = await asyncio.gather(*tasks)
    for res in ress:

        print(res)

asyncio.run(main())
