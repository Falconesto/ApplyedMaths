import math as m

TRUE_EPS = 1e-12


def dichotomy(f, l, r, eps):
    edges = list()
    count = 0
    countF = 0
    edges.append((l, r))
    while abs(r - l) > eps:
        x1 = (l + r) / 2 - (eps / 3)
        x2 = (l + r) / 2 + (eps / 3)
        # print(f"l = {l}, r = {r}, x1 = {x1}, x2 = {x2}, f = {f(x1) - f(x2)}, abs(r - l) = {abs(r - l)}")
        if f(x2) > f(x1):
            r = x2
        else:
            l = x1
        countF+=2
        edges.append((l, r))
        count += 1
    # print(f"l = {l}, r = {r}, abs(r - l) = {abs(r - l)}")
    return (r + l) / 2, edges, count, countF


def golden_cross(f, l, r, eps):
    edges = list()
    count = 0
    countF = 0
    edges.append((l, r))
    k = (m.sqrt(5) - 1) / 2
    x1 = r - k * (r - l)
    x2 = l + k * (r - l)
    iteration_count = 0
    f1 = f(x1)
    f2 = f(x2)
    countF +=2
    while r - l > eps:
        # print(f"x1 = {x1}, x2 = {x2}, f(x1) = {f(x1)} f(x2) = {f(x2)}")
        iteration_count += 1
        if l == x1:  # shift left board
            x1 = x2
            f1 = f2
            x2 = l + k * (r - l)
            f2 = f(x2)
            countF += 1
        elif iteration_count != 1:  # shift right board
            x2 = x1
            x1 = r - k * (r - l)
            f2 = f1
            f1 = f(x1)
            countF += 1
        if f2 > f1:
            r = x2
        else:
            l = x1
        edges.append((l, r))
        count += 1
        # print(f"l = {l}, r = {r}")
    return (l + r) / 2, edges, count, countF


def fibonacci(f, l, r, eps):
    edges = list()
    count = 0
    countF = 0
    edges.append((l, r))
    n = 0
    fib_np1 = 1
    fib_np2 = 1
    while (fib_np1 + fib_np2) <= (r - l) / eps:
        n += 1
        temp = fib_np1
        fib_np1 = fib_np2
        fib_np2 = fib_np2 + temp

    x1 = l + (fib_np2 - fib_np1) / fib_np2 * (r - l)
    x2 = l + fib_np1 / fib_np2 * (r - l)
    f1 = f(x1)
    f2 = f(x2)
    countF += 2

    for i in range(2, n):  # вкурить 2
        # print(f"x1 = {x1}, x2 = {x2}, f(x1) = {f(x1)} f(x2) = {f(x2)}")
        if f2 > f1:
            r = x2
            new_f = f1
        else:
            l = x1
            x1 = x2
            new_f = f2
        if (x1 - l) < (r - x1):
            x2 = r - (x1 - l)
            f1 = new_f
            f2 = f(x2)
            countF += 1
        else:
            x2 = x1
            x1 = l + (r - x2)
            f2 = new_f
            f1 = f(x1)
            countF += 1
        edges.append((l, r))
        count += 1
        # print(f"l = {l}, r = {r}")
    return (r + l) / 2, edges, count, countF


def parabola(f, l, r, eps):
    edges = list()
    count = 0
    countF = 0
    edges.append((l, r))
    x1 = l
    x2 = (l + r) / 2
    x3 = r
    f1 = f(x1)
    f2 = f(x2)
    f3 = f(x3)
    countF += 3

    while (x3 - x1) > eps:
        num = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)
        denum = 2 * ((x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1))
        u = x2 - num / denum
        fu = f(u)
        countF += 1
        if fu > f2:
            if u < x2:
                x1 = u
                f1 = fu
            else:
                x3 = u
                f3 = fu
        else:
            if u < x2:
                x3 = x2
                f3 = f2
            else:
                x1 = x2
                f1 = f2
        x2 = (x1 + x3) / 2
        f2 = f(x2)
        countF += 1
        edges.append((x1, x3))
        count += 1
    return (x1 + x3) / 2, edges, count, countF


def sign(x):
    if x == 0:
        return 0
    return x / abs(x)


def u_from_parabola(x1, x2, x3, f1, f2, f3):
    if x1 > x2:
        x1, x2 = x2, x1
        f1, f2 = f2, f1
    if x2 > x3:
        x2, x3 = x3, x2
        f2, f3 = f3, f2
    if x1 > x2:
        x1, x2 = x2, x1
        f1, f2 = f2, f1
    num = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)
    denum = 2 * ((x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1))
    return x2 - num / denum


def brent(f, a, c, eps):
    edges = list()
    count = 0
    countF = 0
    edges.append((a, c))
    k = (3 - m.sqrt(5)) / 2
    x = w = v = (a + c) / 2
    fx = fw = fv = f(x)
    countF += 1
    d = e = c - a
    while abs(c - a) > eps * 2.1:  # bad precision i think
        # print(f"a = {a}, c = {c}")
        u = None
        g = e
        e = d
        if x != w and x != v and w != v and fx != fw and fx != fv and fw != fv:
            u1 = u_from_parabola(x, w, v, fx, fw, fv)  # do shit: Параболическая аппроксимация, находим u;
            if a + eps < u1 < c - eps and abs(u1 - x) < g / 2:
                u = u1
                d = abs(u - x)

        if u is None:
            if x < (c + a) / 2:
                u = x + k * (c - x)
                d = c - x
            else:
                u = x - k * (x - a)
                d = x - a

        if abs(u - x) < eps:
            u = x + sign(u - x) * eps  # Задаем минимальную близость между u и x
        fu = f(u)
        countF += 1
        if fu <= fx:
            if u >= x:
                a = x
            else:
                c = x
            v = w
            w = x
            x = u
            fv = fw
            fw = fx
            fx = fu
        else:
            if u >= x:
                c = u
            else:
                a = u
            if fu <= fw or w == x:
                v = w
                w = u
                fv = fw
                fw = fu
            elif fu < fv or v == x or v == w:
                v = u
                fv = fu
        edges.append((a, c))
        count += 1
    return x, edges, count, countF


def main():
    f = lambda x: x ** 3 * m.sin(x)

    print("Please select the algorithm :")
    print("1 -- dichotomy")
    print("2 -- golden_cross")
    print("3 -- fibonacci")
    print("4 -- parabola")
    print("5 -- combined brent's method")
    switch = input()
    if switch == "1":
        answer = dichotomy(f, -2, 1, 1e-3)
        res, edges, count, countF = answer
        print("The minimum (x) is -- ", f"{res:.9f}", " -- with f(x)= ", f"{f(res):.9f}")
        print("The number of counting the function is -- ", countF)
        print("By the way, the number of iterations is -- ", count, " -- and here are the actual edges decreases.")
        k = 1
        while k < len(edges):
            a0, b0 = edges[k - 1]
            a1, b1 = edges[k]
            print((b0 - a0) / (b1 - a1))
            k += 1
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x1,",", x2)
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x2-x1)
            # print(i)

    elif switch == "2":
        answer = golden_cross(f, -2, 8, 1e-3)
        res, edges, count, countF = answer
        print("The minimum (x) is -- ", f"{res:.9f}", " -- with f(x)= ", f"{f(res):.9f}")
        print("The number of counting the function is -- ", countF)
        print("By the way, the number of iterations is -- ", count, " -- and here are the actual edges decreases.")
        k = 1
        while k < len(edges):
            a0, b0 = edges[k - 1]
            a1, b1 = edges[k]
            print((b0 - a0) / (b1 - a1))
            k += 1

        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x1,",", x2)
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x2-x1)
            # print(i)

    elif switch == "3":
        answer = fibonacci(f, -2, 1, 1e-3)
        res, edges, count, countF = answer
        print("The minimum (x) is -- ", f"{res:.9f}", " -- with f(x)= ", f"{f(res):.9f}")
        print("The number of counting the function is -- ", countF)
        print("By the way, the number of iterations is -- ", count, " -- and here are the actual edges decreases.")
        k = 1
        while k < len(edges):
            a0, b0 = edges[k - 1]
            a1, b1 = edges[k]
            print((b0 - a0) / (b1 - a1))
            k += 1

        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x1,",", x2)
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x2-x1)
            # print(i)

    elif switch == "4":
        answer = parabola(f, -2, 0.1, 1e-3)
        res, edges, count, countF = answer
        print("The minimum (x) is -- ", f"{res:.9f}", " -- with f(x)= ", f"{f(res):.9f}")
        print("The number of counting the function is -- ", countF)
        print("By the way, the number of iterations is -- ", count, " -- and here are the actual edges decreases.")
        k = 1
        while k < len(edges):
            a0, b0 = edges[k - 1]
            a1, b1 = edges[k]
            print((b0 - a0) / (b1 - a1))
            k += 1

        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x1,",", x2)
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x2-x1)
            # print(i)

    elif switch == "5":
        answer = brent(f, -2, 20, 1e-3)
        res, edges, count, countF = answer
        print("The minimum (x) is -- ", f"{res:.9f}", " -- with f(x)= ", f"{f(res):.9f}")
        print("The number of counting the function is -- ", countF)
        print("By the way, the number of iterations is -- ", count, " -- and here are the actual edges decreases.")
        k = 1
        while k < len(edges):
            a0, b0 = edges[k - 1]
            a1, b1 = edges[k]
            print((b0 - a0) / (b1 - a1))
            k += 1

        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x1,",", x2)
        for i in range(len(edges)):
            x1, x2 = edges[i]
            print(x2-x1)
            # print(i)

    else:
        print("Wrong value for input")

    # print(f"{dichotomy(f, -2, 1, 1e-3):.9f}")  # TODO: fixme sempai. Sempai did it 😎
    # print(f"{golden_cross(f, -2, 1, 1e-3):.9f}")
    # print(f"{fibonacci(f, 3, 6, 1e-3):.9f}")
    # print(f"{parabola(f, 3, 6, 1e-3):.9f}")
    # print(f"{brent(f, 3, 6, 1e-10):.9f}")


if __name__ == '__main__':
    main()
