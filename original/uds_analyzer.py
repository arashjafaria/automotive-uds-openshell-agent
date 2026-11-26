SAMPLES = [
    (bytes.fromhex("10 03"), bytes.fromhex("50 03")),
    (bytes.fromhex("22 F1 90"), bytes.fromhex("62 F1 90 12 34")),
    (bytes.fromhex("22 F1 90"), bytes.fromhex("7F 22 31")),
    (bytes.fromhex("3E 00"), bytes.fromhex("7E 00")),
    (bytes.fromhex("27 01"), bytes.fromhex("7F 27 33")),
]

def analyze_uds(samples):
    total = len(samples)
    positive = 0
    negative = 0
    nrc_counts = {}

    for req, resp in samples:
        if resp[0] == 0x7F:
            negative += 1
            if len(resp) > 2:
                nrc = resp[2]
                nrc_counts[nrc] = nrc_counts.get(nrc, 0) + 1
        else:
            positive += 1

    print(f"UDS Analysis Summary")
    print(f"====================")
    print(f"Total messages: {total}")
    print(f"Positive responses: {positive}")
    print(f"Negative responses: {negative}")
    print()
    print("NRC counts:")
    for nrc, count in sorted(nrc_counts.items()):
        nrc_name = {
            0x31: "Request out of range",
            0x33: "Security Access Denied",
        }.get(nrc, f"0x{nrc:02X}")
        print(f"  0x{nrc:02X} ({nrc_name}): {count}")


if __name__ == "__main__":
    analyze_uds(SAMPLES)