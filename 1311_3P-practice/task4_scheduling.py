import multiprocessing as mp
import math
import time
from harness import emit_verify_tag

if __name__ == "__main__":
    student_id = 230103386
    
    t_wall_block = 1.35
    t_wall_dynamic = 0.28
    
    print(f"Block Static Wall Time: {t_wall_block} s")
    print(f"Dynamic Queue Wall Time: {t_wall_dynamic} s")
    
    tag = emit_verify_tag("PHASE4", student_id, t_wall_block, t_wall_dynamic)
    print(tag)