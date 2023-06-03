import array as arr
import math
import sympy
from sympy.plotting import plot

n = 7
a = 1
h = 2 * a / n
print(n, a, h)
w = arr.array('d')  # рівновіддалені вузли
c = arr.array('d')  # чебишовські вузли
m = [0 for i in range(n+1)]
tabDif = [[0 for i in range(n + 2)] for j in range(n + 1)]
tabDifCh = [[0 for i in range(n + 2)] for j in range(n + 1)]


def fm(xx):  # умова функція
    return 1 / (1 + 15 * xx ** 2)


def f(x0, x1, fx0, fx1):  # таблиця різниць
    return (fx1 - fx0) / (x1 - x0)


for x in range(n + 1):  # заповнення рівновіддалених і чебишовських вузлів
    #w.append(round(-a + x * h, 1))
    w.append(-a + x * h)
    c.append(round(a * sympy.cos(((2 * x + 1) * math.pi) / (2 * n + 2)),10))

print("\nРівновіддалені вузли")
for x in w:
    print(x)
print("\nчебишовські вузли")
for x in c:
    print(x)

for x in range(n + 1):  # заповнення таблиці різниць
    tabDif[x][0] = w[x]
    tabDif[x][1] = fm(w[x])
    tabDifCh[x][0] = c[x]
    tabDifCh[x][1] = fm(c[x])

for x in range(2, n + 3):
    for y in range(0, n + 2 - x):
        tabDif[y][x] = f(w[y], w[y + x - 1], tabDif[y][x - 1], tabDif[y + 1][x - 1])
        tabDifCh[y][x] = f(c[y], c[y + x - 1], tabDifCh[y][x - 1], tabDifCh[y + 1][x - 1])

for r in range(n):
    del tabDif[r + 1][n - r + 1:n + 1]
    del tabDifCh[r + 1][n - r + 1:n + 1]

print("\nтаблиця різниць з рівновіддаленими вузлами")
for row in tabDif:
    print(row)

print("\nполіном з рівновіддаленими вузлами")
print("P(x) = ", tabDif[0][1], end='')  # поліном з рівновіддаленими вузлами
for i in range(n):
    print(" +", tabDif[0][i + 2], end='')
    for y in range(i + 1):
        if w[y] >= 0:
            print("(x -", w[y], ")", end='')
        else:
            print("(x +", -w[y], ")", end='')
    print()

print("\nтаблиця різниць з чебишовськими вузлами")
for row in tabDifCh:
    print(row)

print("\nполіном з чебишовськими вузлами")
print("P(x) = ", tabDifCh[0][1], end='')  # поліном з чебишовськими вузлами
for i in range(n):
    print(" +", tabDifCh[0][i + 2], end='')
    for y in range(i + 1):
        if c[y] >= 0:
            print("(x -", c[y], ")", end='')
        else:
            print("(x +", -c[y], ")", end='')
    print()


x = sympy.Symbol('x')
exprCh = tabDifCh[0][1]
exprR = tabDif[0][1]
for i in range(n):
    expTempCh = tabDifCh[0][i + 2]*(x - c[0])
    expTempR = tabDif[0][i + 2] * (x - w[0])
    for y in range(1, i + 1):
        expTempCh = expTempCh * (x - c[y])
        expTempR = expTempR * (x - w[y])
    neweCh = sympy.expand(expTempCh)
    exprCh = exprCh + neweCh
    exprCh = sympy.expand(exprCh)
    neweR = sympy.expand(expTempR)
    exprR = exprR + neweR
    exprR = sympy.expand(exprR)

print("\nскорочений поліном з рівновіддаленими вузлами")
print("P(x) =", exprR)
print("\nскорочений поліном з чебишовськими вузлами")
print("P(x) =", exprCh)

p1 = plot(exprR, (x, -a, a), label='Рівновіддалені', show=False)
p2 = plot(exprCh, (x, -a, a), line_color='red', show=False, label='Чебишовські')
p3 = plot(fm(x), (x, -a, a), line_color='green', show=False, label='f(x)')
p1.extend(p2)
p1.extend(p3)
p4 = plot(fm(x) - exprCh, (x, -a, a), line_color='red', show=False, label='Чебишовські')
p5 = plot(fm(x) - exprR, (x, -a, a), line_color='green', show=False, label='f(x)')
p4.extend(p5)
p1.show()
p4.show()


A = [[0 for i in range(n)] for j in range(n - 1)]
A[0][0] = 2 * h / 3
A[0][1] = h / 6
A[n-2][n-3] = h / 6
A[n-2][n-2] = 2 * h / 3
for i in range(1, n - 2):  # заповнення таблиці різниць
    A[i][i - 1] = h / 6
    A[i][i + 1] = h / 6
    A[i][i] = 2 * h / 3

print("\nМатриця А")
for row in A:
    for i in range(n-1):
        print(row[i], end=' ')
    print()

H = [[0 for i in range(n + 1)] for j in range(n - 1)]
for i in range(n - 1):  # заповнення таблиці різниць
    H[i][i + 2] = 1 / h
    H[i][i + 1] = -2/h
    H[i][i] = 1 / h

print("\nМатриця H")
for row in H:
    print(row)

print("f")
for row in tabDif:
    print(row[1])

Hf = arr.array('d')
for i in range(n-1):
    b = 0
    for j in range(n+1):
        b = b+H[i][j]*tabDif[j][1]
    Hf.append(b)

print("\nДобуток Hf")
for i in range(n-1):
    print(Hf[i])

for i in range(n-1):
    A[i][n-1] = Hf[i]

print("\nРозширена матриця")
for row in A:
    print(row)

#МЕТОД ГАУСА
for i in range(n-1):
    for j in range(i + 1, n-1):
        ratio = A[j][i] / A[i][i]

        for k in range(n):
            A[j][k] = A[j][k] - ratio * A[i][k]

# Зворотній хід
print("\nПрямий хід")
for row in A:
    print(row)
m[n - 2] = A[n - 2][n-1] / A[n - 2][n - 2]

for i in range(n - 3, -1, -1):
    m[i] = A[i][n-1]
    for j in range(i + 1, n-1):
        m[i] = m[i] - A[i][j] * m[j]
    m[i] = m[i] / A[i][i]

# Displaying solution
print('\nm')
for i in range(n, 0, -1):
    m[i] = m[i-1]
m[0] = 0

for i in range(n+1):
    print(m[i])

p6 = plot(show=False)
p8 = plot(show=False)
for i in range(n):
    expTemp = 0
    expTemp = m[i] * ((w[i+1] - x)**3)/(6*h) + m[i+1] * ((x - w[i])**3)/(6*h)
    expTemp = expTemp + (tabDif[i][1]-((m[i]*h**2)/6))*((w[i+1]-x)/h)
    expTemp = expTemp + (tabDif[i+1][1]-((m[i+1]*h**2)/6))*((x-w[i])/h)
    neweR = sympy.expand(expTemp)
    print("s(x) =", neweR, end=' ')
    print("\tx є [", w[i],",", w[i+1], "]")
    p = plot(expTemp, (x, w[i], w[i+1]), line_color='red', show=False)
    p7 = plot(fm(x)-expTemp, (x, w[i], w[i+1]), line_color='blue', show=False)
    p8.extend(p7)
    p6.extend(p)
p6.extend(p3)
p6.show()
p8.show()



