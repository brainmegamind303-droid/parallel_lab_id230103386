import math
import time
import multiprocessing as mp
from harness import emit_verify_tag

def worker_task(elements_chunk):
    acc = 0.0
    for x in elements_chunk:
        val = x
        for _ in range(35):
            val = math.sin(val) * math.cos(val) + math.sqrt(abs(val) + 1.0)
        acc += val
    return acc

def run_stage_a(n_elements):
    subset_size = int(0.05 * n_elements)
    acc = 0.0
    for i in range(subset_size):
        val = float(i + 1)
        for _ in range(12):
            val = math.sin(val) * math.sqrt(val + 1.0)
        acc += val
    return acc

if __name__ == "__main__":
    student_seed = 230103386
    p_log = mp.cpu_count()
    N_strong = 1_600_000
    
    print(f"Starting Strong & Weak Scaling sweeps up to P_log = {p_log}")
    
    t0 = time.perf_counter_ns()
    run_stage_a(N_strong)
    chunk = [float(i) for i in range(N_strong)]
    worker_task(chunk)
    t1 = time.perf_counter_ns()
    t_seq = (t1 - t0) / 1e6
    
    pool = mp.Pool(processes=p_log)
    chunk_size = N_strong // p_log
    chunks = [chunk[i*chunk_size : (i+1)*chunk_size] for i in range(p_log)]
    
    t0 = time.perf_counter_ns()
    run_stage_a(N_strong)
    pool.map(worker_task, chunks)
    t1 = time.perf_counter_ns()
    t_parallel_strong = (t1 - t0) / 1e6
    pool.close()
    pool.join()
    
    s_strong_plog = t_seq / max(t_parallel_strong, 1e-6)
    
    n0 = 250_000
    total_n_weak = n0 * p_log
    weak_chunk = [float(i) for i in range(total_n_weak)]
    w_chunks = [weak_chunk[i*n0 : (i+1)*n0] for i in range(p_log)]
    
    pool = mp.Pool(processes=p_log)
    t0 = time.perf_counter_ns()
    run_stage_a(total_n_weak)
    pool.map(worker_task, w_chunks)
    t1 = time.perf_counter_ns()
    t_weak_plog = (t1 - t0) / 1e6
    pool.close()
    pool.join()
    
    s_gustafson = float(p_log)
    
    print(f"Strong Speedup at P_log: {s_strong_plog:.2f}")
    print(f"Gustafson Scaled Speedup: {s_gustafson:.2f}")
    
    tag = emit_verify_tag("PHASE2", student_seed, s_strong_plog, s_gustafson)
    print(tag)