from pulp import LpProblem, LpVariable, LpInteger, LpConstraint, LpStatus, LpMinimize

# Az adott konstans változók értékei
c1, c2, c3, c4 = 1, 9, 12, 13  # Konstans értékek

# Egyenletek és optimalizálás (csak az egyenletek teljesítése)
def equations_model():
    # Modell létrehozása (a probléma típusa: minimizálás, mivel nincs célfüggvény, a cél az egyenletek teljesítése)
    prob = LpProblem("EqOptimization", LpMinimize)

    # 12 keresett változó (egész számok, 1 és 16 között)
    x = [LpVariable(f"x{i}", lowBound=1, upBound=16, cat=LpInteger) for i in range(12)]

    # Egyenletek (például kombinált egyenletek konstansokkal) 12 változót keresünk x[0] - x[11]
    prob += x[0] + x[1] + x[2] + x[3] == 34
    prob += x[3] + c3 + x[7] + x[10] == 34
    prob += c4 + x[8] + x[9] + x[10] == 34
    prob += x[0] + c2 + x[6] + c4 == 34
    prob += c1 + x[2] + c3 + x[5] == 34
    prob += x[5] + x[7] + x[9] + x[11] == 34
    prob += x[4] + x[6] + x[8] + x[11] == 34
    prob += x[4] + c2 + x[1] + c1 == 34

    # Korlátozások, hogy a változók ne legyenek egyenlők egymással
    for i in range(12):
        for j in range(i + 1, 12):
            prob += x[i] != x[j]  # A változók ne legyenek egyenlők

    # Korlátozások, hogy a változók ne legyenek egyenlők a konstans változókkal
    for i in range(12):
        prob += x[i] != c1
        prob += x[i] != c2
        prob += x[i] != c3
        prob += x[i] != c4

    # Optimalizálás
    prob.solve()

    # Eredmény kiírása
    if LpStatus[prob.status] == 'Optimal':
        solution = [v.varValue for v in x]
        print(f"Optimalizált megoldás: {solution}")
    else:
        print("Nem található optimális megoldás.")
    
    #Ellenőrzés:
    print("Ellenőrzés:")
    print(solution[0] + solution[1] + solution[2] + solution[3]) #1
    print(solution[3] + c3 + solution[7] + solution[10]) #2
    print(c4 + solution[8] + solution[9] + solution[10]) #3
    print(solution[0] + c2 + solution[6] + c4) #4
    print(c1 + solution[2] + c3 + solution[5]) #5
    print(solution[5] + solution[7] + solution[9] + solution[11]) #6
    print(solution[4] + solution[6] + solution[8] + solution[11]) #7
    print(solution[4] + c2 + solution[1] + c1)

# Optimalizálás
equations_model()
def get_pulp_solution():
    return equations_model()
