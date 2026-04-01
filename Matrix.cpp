#include "Matrix.h"

double* Matrix::aligned_alloc(size_t size) {
	size_t alignment = 32;
	void* ptr = std::aligned_alloc(alignment, size * sizeof(double));

	return reinterpret_cast<double*>(ptr);
}

void Matrix::aligned_dealloc(double* ptr) {
	std::free(ptr);
}

size_t calculate_padding(size_t cols) {
	return (cols % 4 == 0) ? cols : cols + 4 - cols % 4;
}

Matrix::Matrix(size_t rows, size_t cols, double init_val) : data_(nullptr, aligned_dealloc), rows_(rows),
				cols_(cols), padded_cols_(calculate_padding(cols)) {
	double* data = aligned_alloc(rows_ * padded_cols_);
	data_.reset(std::assume_aligned<32>(data));
	
	#pragma omp parallel for
	for (size_t i = 0; i < rows_; ++i)
        #pragma omp parallel for simd
		for (size_t j = 0; j < padded_cols_; ++j)
			data[i * padded_cols_ + j] = init_val;
	#if 0	
	std::cout << reinterpret_cast<uintptr_t>(&(*this)(0, 0)) % 32 << '\n';
	std::cout << reinterpret_cast<uintptr_t>(&(*this)(1, 0)) % 32 << '\n';
	std::cout << reinterpret_cast<uintptr_t>(&(*this)(2, 0)) % 32 << '\n';
	#endif
}

Matrix::Matrix(const Matrix& other) 
    : data_(nullptr, aligned_dealloc),
      rows_(other.rows_), 
      cols_(other.cols_), 
      padded_cols_(other.padded_cols_) {
    
    double* data = aligned_alloc(rows_ * padded_cols_);
    data_.reset(std::assume_aligned<32>(data));
    
	#pragma omp parallel for
    for (size_t i = 0; i < rows_; ++i)
        #pragma omp parallel for simd
        for (size_t j = 0; j < padded_cols_; ++j)
            data_[i * padded_cols_ + j] = other.data_[i * padded_cols_ + j];
}

double Matrix::operator()(size_t row, size_t col) const {
	return data_[row * padded_cols_ + col];
}

double& Matrix::operator()(size_t row, size_t col) {
	return data_[row * padded_cols_ + col];
}

Matrix& Matrix::operator=(const Matrix& other) {
    if (this != &other) {
        rows_ = other.rows_;
        cols_ = other.cols_;
        padded_cols_ = other.padded_cols_;
        
        double* data = aligned_alloc(rows_ * padded_cols_);
        data_.reset(std::assume_aligned<32>(data));
		
		#pragma omp parallel for
        for (size_t i = 0; i < rows_; ++i)
            #pragma omp parallel for simd
            for (size_t j = 0; j < padded_cols_; ++j)
                data_[i * padded_cols_ + j] = other.data_[i * padded_cols_ + j];
    }
    return *this;
}
	
Matrix Matrix::operator+(const Matrix& other) const {
	if (rows_ != other.rows_ || cols_ != other.cols_)
		throw std::invalid_argument("Dimension's dismatch.");
	
	Matrix res(rows_, cols_);

	#pragma omp parallel for
	for (size_t i = 0; i < rows_; ++i)
        #pragma omp parallel for simd
		for (size_t j = 0; j < cols_; ++j)
			res(i, j) = (*this)(i, j) + other(i, j);
		
	return res;
}

Matrix Matrix::operator-(const Matrix& other) const {
	if (rows_ != other.rows_ || cols_ != other.cols_)
		throw std::invalid_argument("Dimension's dismatch.");
	
	Matrix res(rows_, cols_);

	#pragma omp parallel for
	for (size_t i = 0; i < rows_; ++i)
        #pragma omp parallel for simd
		for (size_t j = 0; j < cols_; ++j)
			res(i, j) = (*this)(i, j) - other(i, j);
		
	return res;
}

Matrix Matrix::operator*(const Matrix& other) const {
	if (cols_ != other.rows_)
		throw std::invalid_argument("Dimension's dismatch.");
	
	Matrix res(rows_, other.cols_);

	#pragma omp parallel for collapse(2)
	for (size_t i = 0; i < rows_; ++i)
		for (size_t j = 0; j < other.cols_; ++j) {
			double sum = 0.0;
			#pragma omp simd reduction(+:sum)
			for (size_t k = 0; k < cols_; ++k)
				sum += (*this)(i, k) * other(k, j);
			res(i, j) = sum;
		}
		
	return res;
}

Matrix Matrix::operator*(double scalar) const {
	Matrix res(rows_, cols_);
	
	#pragma omp parallel for
	for (size_t i = 0; i < rows_; ++i)
        #pragma omp parallel for simd
		for (size_t j = 0; j < cols_; ++j)
			res(i, j) = (*this)(i, j) * scalar;
		
	return res;
}

Matrix Matrix::create_identity_matrix(size_t n) {
	Matrix identitity_matrix(n, n);

	#pragma omp parallel for 
	for (int i = 0; i < n; ++i)
		identitity_matrix(i, i) = 1.0;
	
	return identitity_matrix;
}

Matrix Matrix::create_general_matrix(Matrix& identity_matrix, size_t n) {
    Matrix general_matrix(n, 2 * n); 
	
	#pragma omp parallel for
    for (int i = 0; i < n; ++i)
        #pragma omp parallel for simd
        for (int j = 0; j < n; ++j) {
            general_matrix(i, j) = (*this)(i, j);
            general_matrix(i, j + n) = identity_matrix(i, j);
    }
	
    return general_matrix;
}
	
Matrix Matrix::transpose() const {
	Matrix res(cols_, rows_);
	
	#pragma omp parallel for simd collapse(2)
	for (size_t i = 0; i < rows_; ++i)
		for (size_t j = 0; j < cols_; ++j)
			res(j, i) = (*this)(i, j);
		
	return res;
}

Matrix Matrix::inverse() const {
	if (rows_ != cols_)
		throw std::invalid_argument("Matrix must be square.");
	
	size_t n = rows_;
	
	Matrix matrix(*this);
	
	Matrix inverse_matrix = matrix.create_identity_matrix(n);
	
	Matrix general_matrix = matrix.create_general_matrix(inverse_matrix, n);
	
	for (int k = 0; k < n; ++k) {
        double kk = matrix(k, k);
        if (matrix(k, k) != 0) {
			#pragma omp parallel for 
            for (int i = 0; i < 2 * n; ++i)
                general_matrix(k, i) /= kk;
             }
		
		#pragma parallel for
        for (int i = k + 1; i < n; ++i) {
            double c;
            if (general_matrix(k, k) != 0)
                c = general_matrix(i, k) / general_matrix(k, k);
            #pragma omp parallel for simd 
            for (int j = 0; j < 2 * n; ++j)
                general_matrix(i, j) -= general_matrix(k, j) * c;
        }

		#pragma omp parallel for simd collapse(2)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                matrix(i, j) = general_matrix(i, j);
    }

    for (int k = n - 1; k >= 0; --k) {
        double kk = general_matrix(k, k);
        if (kk != 0) {
			#pragma omp parallel for simd
            for (int i = 2 * n - 1; i >= 0; --i)
                general_matrix(k, i) /= kk;
            }

		#pragma omp parallel for
        for (int i = k - 1; i >= 0; --i) {
            double c;
            if (general_matrix(k, k) != 0)
                c = general_matrix(i, k) / general_matrix(k, k);
            #pragma omp parallel for simd 
            for (int j = 2 * n - 1; j >= 0; --j)
                general_matrix(i, j) -= general_matrix(k, j) * c;
        }
    }

	#pragma omp parallel for simd collapse(2) 
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            inverse_matrix(i, j) = general_matrix(i, j + n);

	return inverse_matrix;
}

double Matrix::calculate_determinant() const {
    if (rows_ != cols_)
	    throw std::invalid_argument("Matrix must be square.");
    
	double determinant = 1.0;
	size_t n = rows_;
	
	Matrix matrix(*this);
	
	for (int k = 0; k < n; ++k) {
        double kk = matrix(k, k);

	    #pragma omp parallel for	
        for (int i = k + 1; i < n; ++i) {
            double c;
            if (matrix(k, k) != 0)
                c = matrix(i, k) / matrix(k, k);
			
            #pragma omp parallel for simd
            for (int j = 0; j < n; ++j)
                matrix(i, j) -= matrix(k, j) * c;
        }
    }

	for (int i = 0; i < n; ++i)
		determinant *= matrix(i, i);
	
	return determinant;
}
	
void Matrix::fill_random_values() {
	for (size_t i = 0; i < rows_; ++i)
		#pragma omp simd
		for (size_t j = 0; j < cols_; ++j)
			(*this)(i, j) = rand() % 10;
}
	
std::ostream& operator<<(std::ostream& os, const Matrix& matrix) {
	for (size_t i = 0; i < matrix.rows_; ++i) {
		for (size_t j = 0; j < matrix.cols_; ++j)
			os << matrix(i, j) << ' ';
		os << '\n';
	}
	
	return os;
}

std::istream& operator>>(std::istream& is, Matrix& matrix) {
	for (size_t i = 0; i < matrix.rows_; ++i)
		for (size_t j = 0; j < matrix.cols_; ++j)
			is >> matrix(i, j);
	
	return is;
}
