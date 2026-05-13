import math
import json

SR = 39062.5
DAMPING = 2.0

TALKING_HEDZ = {
    "M0_Q0": [
        {"pole_hz": 9320.9, "radius": 0.975292, "val1": -0.43811, "val2": -0.910165, "val3": 0.459516},
        {"pole_hz": 890.7, "radius": 0.979289, "val1": -0.43811, "val2": 0.892611, "val3": 0.456354},
        {"pole_hz": 1569.6, "radius": 0.977293, "val1": -0.43811, "val2": 0.869758, "val3": 0.437083},
        {"pole_hz": 2348.0, "radius": 0.996945, "val1": -0.43811, "val2": 0.883164, "val3": 0.462725},
        {"pole_hz": 4606.9, "radius": 0.947884, "val1": -0.43811, "val2": 1.152325, "val3": 0.582317},
        {"pole_hz": 199.4, "radius": 0.991178, "val1": -0.43811, "val2": 1.401683, "val3": 0.420546},
    ],
    "M0_Q100": [
        {"pole_hz": 8376.0, "radius": 0.962199, "val1": -0.478394, "val2": -0.520938, "val3": 0.461247},
        {"pole_hz": 201.0, "radius": 0.99216, "val1": -0.478394, "val2": 0.987922, "val3": 0.501463},
        {"pole_hz": 2363.1, "radius": 0.982276, "val1": -0.478394, "val2": 0.960327, "val3": 0.553239},
        {"pole_hz": 2731.8, "radius": 0.985248, "val1": -0.478394, "val2": 0.900986, "val3": 0.504097},
        {"pole_hz": 4782.1, "radius": 0.935439, "val1": -0.478394, "val2": 0.936339, "val3": 0.630415},
        {"pole_hz": 1789.2, "radius": 0.996578, "val1": -0.478394, "val2": 2.888686, "val3": 0.471562},
    ],
    "M100_Q0": [
        {"pole_hz": 10157.9, "radius": 0.999023, "val1": -0.451294, "val2": -1.13824, "val3": 0.53074},
        {"pole_hz": 952.9, "radius": 0.999115, "val1": -0.451294, "val2": 0.954523, "val3": 0.509514},
        {"pole_hz": 1508.9, "radius": 0.999146, "val1": -0.451294, "val2": 0.934424, "val3": 0.490285},
        {"pole_hz": 2210.2, "radius": 0.999176, "val1": -0.451294, "val2": 0.9131, "val3": 0.475355},
        {"pole_hz": 4351.7, "radius": 0.996333, "val1": -0.451294, "val2": 1.309271, "val3": 0.709652},
        {"pole_hz": 157.4, "radius": 0.999146, "val1": -0.451294, "val2": 1.380158, "val3": 0.449588},
    ],
    "M100_Q100": [
        {"pole_hz": 8989.0, "radius": 0.999115, "val1": -0.488525, "val2": -0.694115, "val3": 0.532685},
        {"pole_hz": 194.2, "radius": 0.999359, "val1": -0.488525, "val2": 1.017221, "val3": 0.521186},
        {"pole_hz": 2139.2, "radius": 0.999237, "val1": -0.488525, "val2": 1.022145, "val3": 0.594843},
        {"pole_hz": 2410.6, "radius": 0.999176, "val1": -0.488525, "val2": 0.964846, "val3": 0.540799},
        {"pole_hz": 4403.8, "radius": 0.972284, "val1": -0.488525, "val2": 1.060883, "val3": 0.737424},
        {"pole_hz": 1509.0, "radius": 0.999084, "val1": -0.488525, "val2": 2.898116, "val3": 0.486697},
    ],
}

def float_to_uint16(val):
    if val <= 0: return 0
    if val >= 2.0: return 0xFFFF
    log2 = math.log2(val)
    exp = int(math.floor(log2))
    if exp < -15: exp = -15
    mantissa = val / (2.0 ** exp)
    mantissa_bits = int(round((mantissa - 1.0) * 4096))
    raw = ((exp + 15) << 12) | (mantissa_bits & 0xFFF)
    return raw & 0xFFFF

def encode_stage(s):
    a2 = s["radius"] ** 2
    b2 = a2 - s["val3"]
    a1 = DAMPING * s["radius"] * math.cos(2 * math.pi * s["pole_hz"] / SR)
    b1 = s["val2"] - a1
    c0 = 1 + s["val1"]
    c1 = a1 + s["val2"]
    c2 = b2
    c3 = a2
    c4 = 0.5619
    return [float_to_uint16(c0), float_to_uint16(c1), float_to_uint16(c2), float_to_uint16(c3), float_to_uint16(c4)]

for corner in ["M0_Q0", "M0_Q100", "M100_Q0", "M100_Q100"]:
    stages = TALKING_HEDZ[corner]
    print(f"// {corner}")
    for i, s in enumerate(stages):
        w = encode_stage(s)
        print(f"        0x{w[0]:04X}, 0x{w[1]:04X}, 0x{w[2]:04X}, 0x{w[3]:04X}, 0x{w[4]:04X}, // S{i} {s['pole_hz']:.0f}Hz r={s['radius']:.4f}")