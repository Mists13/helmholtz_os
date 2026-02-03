
import numpy as np

def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc - ad), 2 * (bd + ac), 0],
                     [2 * (bc + ad), aa + cc - bb - dd, 2 * (cd - ab), 0],
                     [2 * (bd - ac), 2 * (cd + ab), aa + dd - bb - cc, 0],
                     [0, 0, 0, 1]])

def translation_matrix(v):
    return np.array([[1, 0, 0, v[0]],
                     [0, 1, 0, v[1]],
                     [0, 0, 1, v[2]],
                     [0, 0, 0, 1]])

def calculate_fk(joints):
    # joints: [j1, j2, j3, j4, j5, j6]
    
    # Base -> J1
    T_0_1 = translation_matrix([0, 0, 0.01]) @ rotation_matrix([0, 0, 1], joints[0])
    
    # J1 -> J2
    T_1_2 = translation_matrix([0, 0, 0.2]) @ rotation_matrix([0, 1, 0], joints[1])
    
    # J2 -> J3
    T_2_3 = translation_matrix([0, 0, 0.25]) @ rotation_matrix([0, 1, 0], joints[2])
    
    # J3 -> J4
    # wrist_1_joint: axis Z
    T_3_4 = translation_matrix([0, 0, 0.2]) @ rotation_matrix([0, 0, 1], joints[3])
    
    # J4 -> J5
    # wrist_2_joint: axis Y
    T_4_5 = translation_matrix([0, 0, 0.15]) @ rotation_matrix([0, 1, 0], joints[4])
    
    # J5 -> J6
    # wrist_3_joint: axis Z
    T_5_6 = translation_matrix([0, 0, 0.12]) @ rotation_matrix([0, 0, 1], joints[5])
    
    T_0_6 = T_0_1 @ T_1_2 @ T_2_3 @ T_3_4 @ T_4_5 @ T_5_6
    
    return T_0_6

poses = [
    [0.0, 0.76, 1.5, 0.0, 0.88, 0.0],
    [0.0, 0.76, 1.55, 0.0, 0.83, 0.0],
    [0.0, 0.78, 1.5, 0.0, 0.86, 0.0],
    [0.0, 0.76, 1.48, 0.0, 0.90, 0.0],
]

print("--- Testing Poses ---")
for i, p in enumerate(poses):
    T = calculate_fk(p)
    pos = T[:3, 3]
    object_pos = np.array([0.45, 0.0, 0.05])
    dist = np.linalg.norm(pos - object_pos)
    print(f"Pose {i} {p}: Pos={pos}, Dist={dist}")
