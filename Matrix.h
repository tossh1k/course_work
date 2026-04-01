#pragma once
#include <iostream>
#include <vector>
#include <memory>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <omp.h>

class Matrix {
	std::unique_ptr<double[], void(*)(double*)> data_;
	size_t rows_;
	size_t cols_;
	size_t padded_cols_;
	
	static double* aligned_alloc(size_t size);
	static void aligned_dealloc(double* ptr);

	Matrix create_identity_matrix(size_t n);
	Matrix create_general_matrix(Matrix& identity_matrix, size_t n);
	
public:
	Matrix(size_t rows, size_t cols, double init_val = 0.0);
	Matrix(const Matrix& other);
	~Matrix() = default;
	
	double operator()(size_t row, size_t col) const;
	double& operator()(size_t row, size_t col);
	Matrix& operator=(const Matrix& other);
	Matrix operator+(const Matrix& other) const;
	Matrix operator-(const Matrix& other) const;
	Matrix operator*(const Matrix& other) const;
	Matrix operator*(double scalar) const;

	Matrix transpose() const;
	Matrix inverse() const;
	double calculate_determinant() const;
	void fill_random_values();
	
	friend std::ostream& operator<<(std::ostream& os, const Matrix& matrix);
	friend std::istream& operator>>(std::istream& is, Matrix& matrix);
};
