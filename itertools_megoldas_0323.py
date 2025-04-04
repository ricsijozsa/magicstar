from itertools import permutations
import time
import streamlit as st

# fix értékek
c1, c2, c3, c4 = 1, 9, 12, 13
numbers = [i for i in range(1, 17) if i not in {c1, c2, c3, c4}]
TOTAL_PERMS = 479001600  # 12 faktoriális

def check_solution(arr):
    return (
        arr[0] + arr[1] + arr[2] + arr[3] == 34 and
        arr[3] + c3 + arr[7] + arr[10] == 34 and
        c4 + arr[8] + arr[9] + arr[10] == 34 and
        arr[0] + c2 + arr[6] + c4 == 34 and
        c1 + arr[2] + c3 + arr[5] == 34 and
        arr[5] + arr[7] + arr[9] + arr[11] == 34 and
        arr[4] + arr[6] + arr[8] + arr[11] == 34 and
        arr[4] + c2 + arr[1] + c1 == 34
    )

def find_magic_star():
    start_time = time.time()
    counter = 0
    solutions = []

    progress = st.progress(0, text="Permutációk feldolgozása...")
    status = st.empty()

    for perm in permutations(numbers, 12):
        counter += 1

        if counter % 100000 == 0:
            elapsed = time.time() - start_time
            percent = counter / TOTAL_PERMS
            progress.progress(percent, text=f"{counter:,} vizsgálva • {int(elapsed)} mp • {int(percent*100)}%")
            status.text(f"Folyamatban: {counter:,} / {TOTAL_PERMS:,}")

        if check_solution(perm):
            solutions.append(list(perm))
            st.info(f"Találat: {len(solutions)} darab eddig ({counter:,}. permutációnál)")

    elapsed = time.time() - start_time
    status.text(f"Kész. {counter:,} permutáció ellenőrizve, idő: {int(elapsed)} mp")
    progress.progress(1.0)

    if solutions:
        return solutions[0]  # visszatérünk az elsővel (az app.py ezt használja)
    return None

def get_brute_force_solution():
    return find_magic_star()
