# prototypes for sharing

from numpy cimport ndarray, uint8_t

cdef bint is_null_datetimelike(v)
cpdef bint is_period(val)

cpdef ndarray[uint8_t] scalar_compare(ndarray[object] values,
                                      object val, object op)
