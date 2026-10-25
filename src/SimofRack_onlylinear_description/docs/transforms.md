# Transformation Matrices - SimofRack_onlylinear

Homogeneous transformation matrices between consecutive frames.
Convention: URDF RPY (XYZ extrinsic / ZYX intrinsic).

## Notation

### Frames

| Index | Link |
|-------|------|
| $L_{0}$ | base_link |
| $L_{1}$ | Top_support |
| $L_{2}$ | Linear_Actuator_X_edited_Component18 |
| $L_{3}$ | Linear_Actuator_X_edited_Component1 |
| $L_{4}$ | Linear_Actuator_Y_Component1 |
| $L_{5}$ | Linear_Actuator_Y_Component18 |
| $L_{6}$ | Component6 |
| $L_{7}$ | Component7 |

### Joint Variables

| Variable | Joint | Type | From | To |
|----------|-------|------|------|----|
| $q_{1}$ | Top_Slider | prismatic (m) | $L_{0}$ | $L_{1}$ |
| $q_{2}$ | Slider_2 | prismatic (m) | $L_{2}$ | $L_{3}$ |
| $q_{3}$ | Slider_2_1 | prismatic (m) | $L_{2}$ | $L_{4}$ |
| $q_{4}$ | Slider_3 | prismatic (m) | $L_{6}$ | $L_{7}$ |

Shorthand: $c_i = \cos(q_i)$, $s_i = \sin(q_i)$

### Kinematic Tree

```
L0: base_link
  |-- [prismatic] Top_Slider (q1)
  |   L1: Top_support
  +-- [fixed] Xslider18_Raack
      L2: Linear_Actuator_X_edited_Component18
        |-- [prismatic] Slider_2 (q2)
        |   L3: Linear_Actuator_X_edited_Component1
        |     +-- [fixed] Xplate_Ymotor
        |         L5: Linear_Actuator_Y_Component18
        +-- [prismatic] Slider_2_1 (q3)
            L4: Linear_Actuator_Y_Component1
              +-- [fixed] Rigid_52
                  L6: Component6
                    +-- [prismatic] Slider_3 (q4)
                        L7: Component7
```

## Transforms

## Top_Slider

$L_{0}$ **base_link** -> $L_{1}$ **Top_support** (prismatic)
  Variable: $q_{1}$

- **origin xyz**: (0.343397, -0.246184, 1.47227) m
- **origin rpy**: (-1.559233, 0, 1.570796) rad
- **axis**: (0, -1, 0)

### Local Transform

$$
T^{0}_{1}(q_{1}) = \begin{bmatrix}
0 & -0.011563 & -0.999933 & 0.343397 \\
1 & 0 & 0 & -0.246184 - q_{1} \\
0 & -0.999933 & 0.011563 & 1.47227 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Xslider18_Raack

$L_{0}$ **base_link** -> $L_{2}$ **Linear_Actuator_X_edited_Component18** (fixed)

- **origin xyz**: (0.976769, -0.294032, 0.262728) m
- **origin rpy**: (0, 0, 1.570796) rad

### Local Transform

$$
T^{0}_{2} = \begin{bmatrix}
0 & -1 & 0 & 0.976769 \\
1 & 0 & 0 & -0.294032 \\
0 & 0 & 1 & 0.262728 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Slider_2

$L_{2}$ **Linear_Actuator_X_edited_Component18** -> $L_{3}$ **Linear_Actuator_X_edited_Component1** (prismatic)
  Variable: $q_{2}$

- **origin xyz**: (0.026448, 0.610209, 0.050742) m
- **origin rpy**: (0, 0, 0) rad
- **axis**: (-1, 0, 0)
- **limits**: [-0.875, 0.01] m

### Local Transform

$$
T^{2}_{3}(q_{2}) = \begin{bmatrix}
1 & 0 & 0 & 0.026448 - q_{2} \\
0 & 1 & 0 & 0.610209 \\
0 & 0 & 1 & 0.050742 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Slider_2_1

$L_{2}$ **Linear_Actuator_X_edited_Component18** -> $L_{4}$ **Linear_Actuator_Y_Component1** (prismatic)
  Variable: $q_{3}$

- **origin xyz**: (0.031448, 0.600139, 0.47665) m
- **origin rpy**: (1.570796, 0, -3.141593) rad
- **axis**: (1, 0, 0)
- **limits**: [-0.85, -0.01] m

### Local Transform

$$
T^{2}_{4}(q_{3}) = \begin{bmatrix}
-1 & 0 & 0 & 0.031448 + q_{3} \\
0 & 0 & 1 & 0.600139 \\
0 & 1 & 0 & 0.47665 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Xplate_Ymotor

$L_{3}$ **Linear_Actuator_X_edited_Component1** -> $L_{5}$ **Linear_Actuator_Y_Component18** (fixed)

- **origin xyz**: (0.031448, -0.060812, 0.177926) m
- **origin rpy**: (1.570796, 0, -3.141593) rad

### Local Transform

$$
T^{3}_{5} = \begin{bmatrix}
-1 & 0 & 0 & 0.031448 \\
0 & 0 & 1 & -0.060812 \\
0 & 1 & 0 & 0.177926 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Rigid_52

$L_{4}$ **Linear_Actuator_Y_Component1** -> $L_{6}$ **Component6** (fixed)

- **origin xyz**: (-0.251316, -0.01, 0.0238) m
- **origin rpy**: (-1.570796, 0, -1.570796) rad

### Local Transform

$$
T^{4}_{6} = \begin{bmatrix}
0 & 0 & 1 & -0.251316 \\
-1 & 0 & 0 & -0.01 \\
0 & -1 & 0 & 0.0238 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Slider_3

$L_{6}$ **Component6** -> $L_{7}$ **Component7** (prismatic)
  Variable: $q_{4}$

- **origin xyz**: (0, 0.007, 0.284666) m
- **origin rpy**: (3.141593, 0, 3.141593) rad
- **axis**: (-1, 0, 0)
- **limits**: [0.01, 0.075] m

### Local Transform

$$
T^{6}_{7}(q_{4}) = \begin{bmatrix}
-1 & 0 & 0 & -q_{4} \\
0 & 1 & 0 & 0.007 \\
0 & 0 & -1 & 0.284666 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

---

## Global Transform Chains

Transform from root $L_0$ to any link, as product of local transforms along the kinematic chain.

$$T^{0}_{3} = T^{0}_{2} \cdot T^{2}_{3}(q_{2})\quad (L_0 \to L_{3}: \text{Linear_Actuator_X_edited_Component1})$$

$$T^{0}_{4} = T^{0}_{2} \cdot T^{2}_{4}(q_{3})\quad (L_0 \to L_{4}: \text{Linear_Actuator_Y_Component1})$$

$$T^{0}_{5} = T^{0}_{2} \cdot T^{2}_{3}(q_{2}) \cdot T^{3}_{5}\quad (L_0 \to L_{5}: \text{Linear_Actuator_Y_Component18})$$

$$T^{0}_{6} = T^{0}_{2} \cdot T^{2}_{4}(q_{3}) \cdot T^{4}_{6}\quad (L_0 \to L_{6}: \text{Component6})$$

$$T^{0}_{7} = T^{0}_{2} \cdot T^{2}_{4}(q_{3}) \cdot T^{4}_{6} \cdot T^{6}_{7}(q_{4})\quad (L_0 \to L_{7}: \text{Component7})$$

