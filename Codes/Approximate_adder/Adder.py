import numpy as np

def full_adder(a, b, cin):
    """Implements a 1-bit full adder"""
    sum_bit = (a ^ b) ^ cin
    carry_out = (a & b) | (cin & (a ^ b))
    return sum_bit, carry_out

def ripple_carry_adder(a, b, n, cin=0):
    """Performs n-bit Ripple Carry Addition using full adders"""
    carry = cin  # Carry-in is now controlled externally
    sum_result = ""

    for i in range(n - 1, -1, -1):  # Process from LSB to MSB
        bit_a = int(a[i])
        bit_b = int(b[i])
        sum_bit, carry = full_adder(bit_a, bit_b, carry)
        sum_result = str(sum_bit) + sum_result  # Concatenate sum bits

    return sum_result, carry  # Return final sum and carry out

def approximate_adder(A, B):
    """
    Perform approximate addition:
    - USA (Upper Significant Accurate, 4 bits) with Cin = C_predict
    - LSA (Lower Significant Accurate, uses 4-bit RCA adder)
    - Approximate Logic (OR operation on last 8 bits)
    """
    # Convert decimal to 16-bit binary
    A_bin = decimal_to_16bit_binary(A)
    B_bin = decimal_to_16bit_binary(B)

    # **Splitting the input into sections**
    USA_part_A, LSA_part_A, Approx_part_A = A_bin[:4], A_bin[4:8], A_bin[8:]
    USA_part_B, LSA_part_B, Approx_part_B = B_bin[:4], B_bin[4:8], B_bin[8:]

    # **Compute C_predict from first TWO bits of LSA section (AND operation)**
    C_predict_1 = (int(Approx_part_A[0]) & int(Approx_part_B[0]))

    # **LSA section:** Accurate Ripple Carry Adder (RCA) with Cin = 0
    LSA_sum, Carry_out_LSA = ripple_carry_adder(LSA_part_A, LSA_part_B, 4, cin=C_predict_1)

    # **Compute C_predict from first TWO bits of LSA section (AND operation)**
    C_predict = (int(LSA_part_A[0]) & int(LSA_part_B[0])) & (int(LSA_part_A[1]) & int(LSA_part_B[1]))

    # **Compute C_predict_actual = (~C_predict) & Carry_out_LSA**
    C_predict_actual = (1 - C_predict) & Carry_out_LSA  # Negation (~) in binary (1 - value)

    # **USA section:** Uses `C_predict` as Cin
    USA_sum, _ = ripple_carry_adder(USA_part_A, USA_part_B, 4, cin=C_predict)

    # **Modify the LSB of USA_sum by adding C_predict_actual**
    USA_sum_list = list(USA_sum)  # Convert string to list for modification
    LSB = int(USA_sum_list[-1])  # Extract LSB
    new_LSB, _ = full_adder(LSB, C_predict_actual, 0)  # Add C_predict_actual
    USA_sum_list[-1] = str(new_LSB)  # Replace LSB
    USA_sum = "".join(USA_sum_list)  # Convert back to string

    # **Approximate Logic section:** Apply OR operation on last 8 bits
    Approximate_sum = "".join(str(int(Approx_part_A[i]) | int(Approx_part_B[i])) for i in range(8))

    # **Final sum**
    S = USA_sum + LSA_sum + Approximate_sum

    # Convert final result back to decimal
    final_decimal = binary_to_decimal(S)
    return final_decimal  # Return binary and decimal result


def approximate_proposed_adder(A, B):
    """
    Perform approximate addition with:
    - USA (Upper Significant Accurate, 4 bits) with Cin = C_predict
    - LSA (Lower Significant Accurate, 8-bit RCA adder)
    - Approximate Logic (OR operation on last 4 bits)
    """
    # Convert decimal to 16-bit binary
    A_bin = decimal_to_16bit_binary(A)
    B_bin = decimal_to_16bit_binary(B)

    # **New segment sizes: USA = 4, LSA = 8, Approx = 4**
    USA_part_A, LSA_part_A, Approx_part_A = A_bin[:4], A_bin[4:12], A_bin[12:]
    USA_part_B, LSA_part_B, Approx_part_B = B_bin[:4], B_bin[4:12], B_bin[12:]

    # **Compute C_predict from first TWO bits of LSA section (AND operation)**
    C_predict_1 = (int(Approx_part_A[0]) & int(Approx_part_B[0]))

    # **LSA section:** Accurate 8-bit Ripple Carry Adder (RCA) with Cin = 0
    LSA_sum, Carry_out_LSA = ripple_carry_adder(LSA_part_A, LSA_part_B, 8, cin=C_predict_1)

    # **Compute C_predict from first TWO bits of LSA section**
    C_predict = (int(LSA_part_A[0]) & int(LSA_part_B[0])) & (int(LSA_part_A[1]) & int(LSA_part_B[1]))

    # **Compute C_predict_actual = (~C_predict) & Carry_out_LSA**
    C_predict_actual = (1 - C_predict) & Carry_out_LSA  # Negation (~) in binary

    # **USA section:** Uses `C_predict` as Cin
    USA_sum, _ = ripple_carry_adder(USA_part_A, USA_part_B, 4, cin=C_predict)

    # **Modify the LSB of USA_sum by adding C_predict_actual**
    USA_sum_list = list(USA_sum)  # Convert string to list
    LSB = int(USA_sum_list[-1])  # Extract LSB
    new_LSB, _ = full_adder(LSB, C_predict_actual, 0)  # Add C_predict_actual
    USA_sum_list[-1] = str(new_LSB)  # Replace LSB
    USA_sum = "".join(USA_sum_list)  # Convert back to string

    # **Approximate Logic section:** Apply OR operation on last 4 bits
    Approximate_sum = "".join(str(int(Approx_part_A[i]) | int(Approx_part_B[i])) for i in range(4))

    # **Final sum**
    S = USA_sum + LSA_sum + Approximate_sum

    # Convert final result back to decimal
    final_decimal = binary_to_decimal(S)
    return final_decimal

def Aprx_propose_adder_1(a, b, c, d):
    # Convert inputs to Python int to avoid NumPy uint8 issues
    a1, b1, c1, d1 = int(a), int(b), int(c), int(d)

    # Perform approximate addition
    y = a1+b1+c1-d1
    out = y//2
    z = DTB_9(out)
    output = decimal((z[1],z[2],z[3],z[4],z[5],z[6],z[7],z[8]))
    # Perform division and ensure values stay within uint8 range

    return output
