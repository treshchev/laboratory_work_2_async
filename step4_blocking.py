"""Шаг 4. Блокировка event loop (дополнительное задание)."""

import asyncio
import time

from timer import log, print_time

CLIENTS = [
    ("alice", 0.5),
    ("bob", 5.0),
    ("carol", 0.5),
    ("dave", 0.5),
    ("eve", 0.5),
]

# Тяжелая синхронная функция, которая грузит процессор (CPU)
def heavy_compute(duration: float) -> None:
    start = time.time()
    while time.time() - start < duration:
        pass  # Крутим пустой цикл, нагружая CPU.

# ПЛОХО: вызов этой функции заблокирует весь event loop
async def handle_request_blocking(client: str, duration: float) -> None:
    log(f"{client}: запрос принят")
    if client == "bob":
        heavy_compute(duration)  # Блокирует всё!
    else:
        await asyncio.sleep(duration)
    log(f"{client}: ответ отправлен")

# ХОРОШО: выносим тяжелую функцию в отдельный поток
async def handle_request_fixed(client: str, duration: float) -> None:
    log(f"{client}: запрос принят")
    if client == "bob":
        await asyncio.to_thread(heavy_compute, duration)
    else:
        await asyncio.sleep(duration)
    log(f"{client}: ответ отправлен")

async def main() -> None:
    print("--- 4а: ПЛОХО (Блокировка event loop) ---")
    with print_time():
        tasks = [handle_request_blocking(c, d) for c, d in CLIENTS]
        await asyncio.gather(*tasks)

    print("\n--- 4б: ХОРОШО (Вынос в отдельный поток) ---")
    with print_time():
        tasks = [handle_request_fixed(c, d) for c, d in CLIENTS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())