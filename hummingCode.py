import pandas as pd


def make_data_with_parity_slot(data):
    result_data = ""
    result_parity = []

    tracking_data = 0
    index = 1
    exponent = 0
    while (tracking_data < len(data)):
        if (index == pow(2, exponent)):
            result_data += "_"
            result_parity.append(pow(2, exponent))
            exponent += 1
        else:
            result_data += data[tracking_data]
            tracking_data += 1
        index += 1
    return result_data[::-1], result_parity


def make_index_coordinate(data):
    index_result = []
    index_data = 1
    exponent = 0
    for x in data:
        if (x == "_"):
            index_result.append(f"p{pow(2, exponent)}")
            exponent += 1
        else:
            index_result.append(f"d{index_data}")
            index_data += 1
    return index_result


def find_parity(data, p, coor):
    stepper = 0
    index = p
    d_summer = ""
    num_summer = ""
    result_xor = 0
    while (index < len(data) + 1):
        d_summer += f"{coor[index-1]}"
        num_summer += f"{data[index-1]}"
        if (data[index - 1] != "_"):
            result_xor ^= int(data[index - 1])
        stepper += 1
        if (stepper >= p):
            index += p
            stepper = 0
        index += 1
        if (index < len(data) + 1):
            d_summer += " + "
            num_summer += " + "
    return d_summer, num_summer, result_xor


def humming_code(input_data):
    output_msg = ""
    input_data = input_data.replace(" ", "")
    data_with_parity, parity = make_data_with_parity_slot(input_data[::-1])
    index_coordinate = make_index_coordinate(data_with_parity[::-1])
    output_msg += f"\nData Bit Diterima:\n{input_data}"
    output_msg += f"\nSlot Paritas:\n{data_with_parity}"
    output_msg += f"\nDaftar Paritas:\n{parity}\n"
    #print(f"Koordinat Posisi:\n{index_coordinate[::-1]}")

    result_data = list(data_with_parity[::-1])
    for p in parity:
        d_sum, num_sum, res_xor = find_parity(data_with_parity[::-1], p,
                                              index_coordinate)
        result_data[p - 1] = str(res_xor)
        output_msg += f"\nPerumusan:\n{d_sum}"
        output_msg += f"\nPenjejakan:\n{num_sum}"
        output_msg += f"\nBit Paritas ke-{p}:\n{res_xor}\n"
    result_data_as_key = result_data[::-1]
    base_coor_table = dict(zip(index_coordinate[::-1], result_data_as_key))
    coor_table = pd.DataFrame(base_coor_table, index=[0])

    batas_akhir = 10
    for i in range(0, len(coor_table.columns), 10):
        output_msg += f"{coor_table.iloc[:, i:batas_akhir].to_string(index=False)}\n"
        batas_akhir += 10
    result_data = "".join(result_data[::-1])
    output_msg += f"\nData yang dikirimkan: {result_data}"

    return output_msg
