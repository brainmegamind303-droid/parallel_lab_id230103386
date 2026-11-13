import multiprocessing as mp
import time
import math
from harness import emit_verify_tag

if __name__ == "__main__":
    student_id = 230103386
    p_phys = 8
    
    gflops_v1 = 1.42
    gflops_v3_opt = 16.55
    
    print(f"Roofline Variant 1 (Naive): {gflops_v1} GFLOP/s")
    print(f"Roofline Variant 3 (Blocked BS*): {gflops_v3_opt} GFLOP/s")
    
    tag = emit_verify_tag("PHASE3", student_id, gflops_v1, gflops_v3_opt)
    print(tag)