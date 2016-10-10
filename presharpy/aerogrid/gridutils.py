#
import numpy as np
import scipy.linalg


def unit_vector(vector):
    return vector/np.linalg.norm(vector)


def skew(vector):
    if not vector.size == 3:
        raise Exception('The input vector is not 3D')

    matrix = np.zeros((3, 3))
    matrix[0, 1] = -vector[2]
    matrix[1, 0] = vector[2]
    matrix[2, 0] = -vector[1]
    matrix[0, 2] = vector[1]
    matrix[1, 2] = -vector[0]
    matrix[2, 1] = vector[0]
    return matrix


def crv_from_vectors(veca, vecb):
    # import pdb;pdb.set_trace()
    if np.linalg.norm(np.cross(veca,vecb)) < 1e-8:
        axis = unit_vector(veca)
    else:
        axis = np.cross(veca,vecb)/np.linalg.norm(np.cross(veca, vecb))
    angle = np.arccos(np.dot(unit_vector(veca), unit_vector(vecb)))
    return axis*angle


def crv2rot(crv):
    rot = np.eye(3)
    if np.linalg.norm(crv) < 1e-8:
        return rot

    crv_norm = np.linalg.norm(crv)
    rot += (np.sin(crv_norm)/crv_norm)*skew(crv)
    rot += (1 - np.cos(crv_norm))/(crv_norm)*np.dot(skew(crv), skew(crv))
    return rot


if __name__ == '__main__':
    pass