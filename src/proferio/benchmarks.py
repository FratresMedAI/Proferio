import time
import psutil


def benchmark_call(callable_fn, *args, **kwargs):
    start = time.perf_counter()
    out = callable_fn(*args, **kwargs)
    end = time.perf_counter()
    mem = psutil.virtual_memory().percent
    return {
        "latency_sec": round(end - start, 4),
        "memory_percent": mem,
        "output": out,
    }
