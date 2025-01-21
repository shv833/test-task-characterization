import struct
from collections import deque


HEADER_HANDLERS = {
    "MIR": lambda header, f: {
        "header": header,
        "temperature": struct.unpack("f", f.read(4))[0],
        "operator": f.read(20).decode("ascii").strip("\x00"),
    },
    "PRR": lambda header, f: {
        "header": header,
        "part_number": struct.unpack("I", f.read(4))[0],
        "status": struct.unpack("B", f.read(1))[0],
    },
    "PTR": lambda header, f: {
        "header": header,
        "test_name": f.read(20).decode("ascii").strip("\x00"),
        "test_value": struct.unpack("f", f.read(4))[0],
        "low_limit": struct.unpack("f", f.read(4))[0],
        "high_limit": struct.unpack("f", f.read(4))[0],
        "status": struct.unpack("B", f.read(1))[0],
    },
}


def decode_binary_file(file_stream) -> list:
    decoded_data = deque()

    while chunk := file_stream.read(4):
        try:
            header = chunk.decode("ascii").strip("\x00")
            handler = HEADER_HANDLERS.get(header)
            if handler:
                decoded_data.append(handler(header, file_stream))
            # else:
            #     decoded_data.append(
            #         {"header": "UNKNOWN", "header": header, "chunk": chunk}
            #     )
        except Exception as e:
            # decoded_data.append({"error": str(e), "chunk": chunk})
            ...
    return list(decoded_data)


def encode_data_to_binary_file(data, output_stream):
    cleared_data = [{k: v for k, v in i.items() if v is not None} for i in data]
    print(cleared_data)
    for item in cleared_data:
        header = item.get("header", "").encode("ascii")
        output_stream.write(header.ljust(4, b"\x00"))

        if header.strip(b"\x00").decode("ascii") == "MIR":
            output_stream.write(struct.pack("f", item.get("temperature", 0.0)))
            output_stream.write(
                item.get("operator", "").ljust(20, "\x00").encode("ascii")
            )
        elif header.strip(b"\x00").decode("ascii") == "PRR":
            output_stream.write(struct.pack("I", item.get("part_number", 0)))
            output_stream.write(struct.pack("B", item.get("status", 0)))
        elif header.strip(b"\x00").decode("ascii") == "PTR":
            output_stream.write(
                item.get("test_name", "").ljust(20, "\x00").encode("ascii")
            )
            output_stream.write(struct.pack("f", item.get("test_value", 0.0)))
            output_stream.write(struct.pack("f", item.get("low_limit", 0.0)))
            output_stream.write(struct.pack("f", item.get("high_limit", 0.0)))
            output_stream.write(struct.pack("B", item.get("status", 0)))
