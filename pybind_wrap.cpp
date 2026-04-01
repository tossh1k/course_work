#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "Matrix.h"
#include <iomanip>

PYBIND11_MODULE(Matrix, m) {
    pybind11::class_<Matrix>(m, "Matrix")
        .def(pybind11::init<size_t, size_t, double>(),
             pybind11::arg("rows"), pybind11::arg("cols"), pybind11::arg("init_values") = 0.0)
        .def(pybind11::init<const Matrix&>())

        .def("__getitem__", [](const Matrix& m, std::pair<size_t, size_t> idx) {
            return m(idx.first, idx.second);
        })
        .def("__setitem__", [](Matrix& m, std::pair<size_t, size_t> idx, double value) {
            m(idx.first, idx.second) = value;
        })

        .def(pybind11::self + pybind11::self)
        .def(pybind11::self - pybind11::self)
        .def(pybind11::self * pybind11::self)
        .def(pybind11::self * double())

        .def("transpose", &Matrix::transpose)
        .def("inverse", &Matrix::inverse)
        .def("calculate_determinant", &Matrix::calculate_determinant)
        .def("fill_random", &Matrix::fill_random_values)
        
        .def("__copy__", [](const Matrix& self) {
            return Matrix(self);
        })
        .def("assign", &Matrix::operator=)

        .def("__str__", [](const Matrix& m) {
            std::ostringstream oss;
            oss << std::setprecision(4) << m;
            return oss.str();
        });
}
