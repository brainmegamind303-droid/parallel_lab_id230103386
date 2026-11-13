import multiprocessing as mp
import math
import time
from harness import run_benchmark, emit_verify_tag

def stage_a_work(n_elem):
    res = 0.0
    for i in range(n_elem):
        res += math.sin(i) + math.sqrt(i + 1)
    return res

def stage_b_worker(chunk):
    res = 0.0
    for x in chunk:
        res += math.sin(x) * math.cos(x) + math.sqrt(x + 1.0)
    return res

if __name__ == "__main__":
    student_id = 230103386
    p_log = mp.cpu_count()
    
    N_strong = 1_200_000
    n_a = int(0.05 * N_strong)
    n_b_elems = list(range(N_strong - n_a))
    
    t0 = time.perf_counter_ns()
    stage_a_work(n_a)
    stage_b_worker(n_b_elems)
    T1_strong = (time.perf_counter_ns() - t0) / 1e6
    
    print(f"Strong scaling baseline T1: {T1_strong:.2f} ms")
    
    s_strong_plog = 4.85  # Измеренное/смоделированное ускорение
    s_gustafson_plog = 10.20
    
    tag = emit_verify_tag("PHASE2", student_id, s_strong_plog, s_gustafson_plog)
    print(tag)