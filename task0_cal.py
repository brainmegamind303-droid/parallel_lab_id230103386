import multiprocessing as mp
import time
from harness import emit_verify_tag

def calibration_benchmark():
    iterations = 2_000_000
    t0 = time.perf_counter_ns()
    for _ in range(iterations):
        _ = time.perf_counter_ns()
    t1 = time.perf_counter_ns()
    return (t1 - t0) / iterations

if __name__ == "__main__":
    student_seed = 230103386
    p_count = mp.cpu_count()
    print(f"Logical Cores / Processors: {p_count}")

    avg_ns = calibration_benchmark()
    print(f"Average timer call latency: {avg_ns:.2f} ns")

    tag = emit_verify_tag("PHASE0", student_seed, float(p_count), avg_ns)
    print(tag)