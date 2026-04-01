import Matrix

m1 = Matrix.Matrix(3, 3, 1.0)
m2 = Matrix.Matrix(3, 3)
m2.fill_random()

m3 = m1 + m2
m4 = m2 - m1
m5 = m1 * m2
m6 = m1 * 3

transposed = m2.transpose()
inverse = m2.inverse()
det = m2.calculate_determinant()

print(m1)
print(m2)
print(m3)
print(m4)
print(m5)
print(m6)
print(transposed)
print(inverse)
print(int(det))
