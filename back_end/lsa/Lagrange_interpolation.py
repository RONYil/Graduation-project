from sympy import symbols, simplify

def lagrange_interpolation_polynomial(x_values, y_values):
    x = symbols('x')
    result = 0

    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if j != i:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term

    return simplify(result)

# 给定的数据点
x_values = [0, 1, 5, 10, 15, 20]
y_values = [0, 838/1587, 1287/1587, 1377/1587, 1384/1587, 1438/1587]

# 获取插值多项式
interpolation_polynomial = lagrange_interpolation_polynomial(x_values, y_values)

# 输出插值多项式
print("Interpolation Polynomial:")
print(interpolation_polynomial)


