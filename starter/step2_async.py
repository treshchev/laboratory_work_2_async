"""Шаг 2. Переписываем на asyncio.

Задание 2а:
  1. Сделайте work корутиной (async def).
  2. Замените time.sleep на await asyncio.sleep.
  3. Сделайте main корутиной и вызовите в ней work через await в цикле.
  4. Запустите через asyncio.run.

Замерьте время. Изменилось ли оно по сравнению с шагом 1? Почему?

Задание 2б:
  Перепишите main так, чтобы все 10 задач ждали одновременно.
  Подсказка: asyncio.gather. Что изменилось в порядке вывода?
"""

import asyncio

from timer import print_time


async def work(n: int) -> None:
    print(f"start {n}")
    await asyncio.sleep(1)
    print(f"done {n}")


# --- 2а: await в цикле, всё ещё последовательно (~10 с) --------------------
# async def main() -> None:
#     for n in range(1, 11):
#         await work(n)


# --- 2б: все задачи ждут одновременно через gather (~1 с) -------------------
async def main() -> None:
    coroutines = [work(n) for n in range(1, 11)]
    await asyncio.gather(*coroutines)


# --- дополнительно: то же самое через create_task ---------------------------
# async def main() -> None:
#     tasks = [asyncio.create_task(work(n)) for n in range(1, 11)]
#     for task in tasks:
#         await task


if __name__ == "__main__":
    with print_time():
        asyncio.run(main())