// #include <python3.8/Python.h>
#include <Python.h>
#include "AnytimeFrenetOptimalTrajectory.h"

typedef struct {
    PyObject_HEAD
    AnytimeFrenetOptimalTrajectory *fot;
} FotPlanner;

typedef struct{
    PyObject_HEAD
    FrenetPath *path;
} FotPath;

PyObject *FotPlanner_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int FotPlanner_init(PyObject *self, PyObject *args, PyObject *kwds);
void FotPlanner_dealloc(FotPlanner *self);

static PyObject *method_async_plan(PyObject *self, PyObject *args);
static PyObject *method_get_path(PyObject *self, PyObject *args);
static PyObject *method_stop_plan(PyObject *self, PyObject *args);