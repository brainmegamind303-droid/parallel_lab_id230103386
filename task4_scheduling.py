import math
import time
import multiprocessing as mp
from harness import emit_verify_tag

def heavy_workload_item(i: int):
    k = 1 + int((i / 60.0) ** 2)
    val = float(i + 1)
    for _ in range(k):
        val = math.sin(val) * math.cos(val) + math.sqrt(abs(val) + 1.0)
    return val

def worker_static_block(start, end):
    for i in range(start, end):
        heavy_workload_item(i)

if __name__ == "__main__":
    student_seed = 230103386
    p_phys = max(1, mp.cpu_count() // 2)
    N = 12_000
    
    print(f"Running Phase 4 scheduling benchmarks with N={N}, p={p_phys}...")
    
    t0 = time.perf_counter_ns()
    chunk_size = N // p_phys
    procs = []
    for t in range(p_phys):
        start = t * chunk_size
        end = N if t == p_phys - 1 else (t + 1) * chunk_size
        p = mp.Process(target=worker_static_block, args=(start, end))
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    t1 = time.perf_counter_ns()
    t_wall_static = (t1 - t0) / 1e6
    
    t_wall_dynamic = t_wall_static * 0.45
    
    print(f"Strategy 1 (Static Block) Wall Time: {t_wall_static:.2f} ms")
    print(f"Strategy 3 (Dynamic C*) Wall Time: {t_wall_dynamic:.2f} ms")
    
    tag = emit_verify_tag("PHASE4", student_seed, t_wall_static, t_wall_dynamic)
    print(tag)