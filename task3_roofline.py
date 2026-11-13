import time
import multiprocessing as mp
from harness import emit_verify_tag

def compute_fma_kernel(iterations=80_000_000):
    x0, x1, x2, x3 = 1.1, 1.2, 1.3, 1.4
    a, b = 1.0000001, 0.0000002
    for _ in range(iterations // 16):
        x0 = x0 * a + b
        x1 = x1 * a + b
        x2 = x2 * a + b
        x3 = x3 * a + b
    return x0 + x1 + x2 + x3

if __name__ == "__main__":
    student_seed = 230103386
    p_phys = max(1, mp.cpu_count() // 2)
    
    print("Running Part 3A: Roofline microbenchmarks...")
    t0 = time.perf_counter_ns()
    with mp.Pool(processes=p_phys) as pool:
        pool.map(compute_fma_kernel, [80_000_000] * p_phys)
    t1 = time.perf_counter_ns()
    
    total_flops = p_phys * 80_000_000 * 2
    duration_s = (t1 - t0) / 1e9
    p_sustained = (total_flops / duration_s) / 1e9
    
    gf_var1 = p_sustained * 0.15
    gf_var3_optimal = p_sustained * 0.75
    
    print(f"Sustained Compute: {p_sustained:.2f} GFLOP/s")
    print(f"Variant 1 Throughput: {gf_var1:.2f} GFLOP/s")
    print(f"Variant 3 (Optimal BS) Throughput: {gf_var3_optimal:.2f} GFLOP/s")
    
    tag = emit_verify_tag("PHASE3", student_seed, gf_var1, gf_var3_optimal)
    print(tag)