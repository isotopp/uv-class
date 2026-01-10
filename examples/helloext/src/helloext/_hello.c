#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *hellop(PyObject *self, PyObject *args) {
    const char *name = NULL;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    PySys_WriteStdout("Hello, %s\n", name);
    Py_RETURN_NONE;
}

static PyObject *hellos(PyObject *self, PyObject *args) {
    const char *name = NULL;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    return PyUnicode_FromFormat("Hello, %s", name);
}

static PyMethodDef HelloMethods[] = {
    {"hellop", hellop, METH_VARARGS, "Print Hello, {name} to stdout."},
    {"hellos", hellos, METH_VARARGS, "Return Hello, {name} as a string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "_hello",
    "Example CPython extension module.",
    -1,
    HelloMethods
};

PyMODINIT_FUNC PyInit__hello(void) {
    return PyModule_Create(&hellomodule);
}

