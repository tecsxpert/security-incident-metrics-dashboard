from concurrent.futures import ThreadPoolExecutor, TimeoutError


executor = ThreadPoolExecutor(max_workers=4)


def run_with_timeout(func, fallback, timeout: float = 3.0):
    try:
        future = executor.submit(func)
        return future.result(timeout=timeout)
    except TimeoutError:
        print(" TIMEOUT TRIGGERED")
        return fallback()
    except Exception as e:
        print(" ERROR IN TIMEOUT:", str(e))
        return fallback()