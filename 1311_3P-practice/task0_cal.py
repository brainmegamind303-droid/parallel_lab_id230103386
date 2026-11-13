import multiprocessing as mp
import time
from harness import emit_verify_tag

if __name__ == "__main__":
    student_id = 230103386
    iters = 1_000_000
    t_start = time.perf_counter_ns()
    for _ in range(iters):
        _ = time.perf_counter_ns()
    t_end = time.perf_counter_ns()

    avg_ns = (t_end - t_start) / iters
    print(f"Average time.perf_counter_ns() call latency: {avg_ns:.2f} ns")

    tag = emit_verify_tag("PHASE0", student_id, avg_ns, 0.0)
    print(tag)