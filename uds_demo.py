"""Synthetic UDS response classifier for educational, non-production use.

This is a newly written, minimal demonstration to accompany the OpenCode agent
configuration. It is not a copy of the user's earlier local uds_analyzer.py.
The CSV contains already reassembled UDS response payloads, NOT raw CAN frames.
"""

import argparse
import csv
import json
from pathlib import Path

NRC_DESCRIPTIONS = {
    0x10: "General Reject",
    0x11: "Service Not Supported",
    0x12: "SubFunction Not Supported",
    0x22: "Conditions Not Correct",
    0x31: "Request Out Of Range",
    0x33: "Security Access Denied",
    0x78: "Response Pending",
}


def classify_response(payload_hex: str) -> dict:
    """Classify one simplified UDS *response payload* expressed as hex bytes."""
    try:
        payload = bytes.fromhex(payload_hex)
    except ValueError as exc:
        raise ValueError(f"Invalid hexadecimal payload: {payload_hex!r}") from exc
    if not payload:
        raise ValueError("UDS response payload must not be empty")
    if payload[0] == 0x7F:
        if len(payload) < 3:
            raise ValueError("Negative response requires 7F, request SID, and NRC")
        sid, nrc = payload[1], payload[2]
        return {
            "result": "negative",
            "request_sid": f"0x{sid:02X}",
            "response_sid": "0x7F",
            "nrc": f"0x{nrc:02X}",
            "description": NRC_DESCRIPTIONS.get(nrc, "Unmapped NRC"),
        }
    sid = payload[0]
    if not 0x50 <= sid <= 0x7E:
        return {
            "result": "unclassified",
            "request_sid": None,
            "response_sid": f"0x{sid:02X}",
            "nrc": None,
            "description": "Unknown/unsupported response type",
        }
    return {
        "result": "positive",
        "request_sid": f"0x{sid-0x40:02X}",
        "response_sid": f"0x{sid:02X}",
        "nrc": None,
        "description": "Positive response",
    }


def analyze_csv(file_path: Path) -> list[dict]:
    with file_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"timestamp", "can_id", "uds_payload"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must have columns {sorted(required)}")
        return [
            {
                "timestamp": row["timestamp"],
                "can_id": row["can_id"],
                "uds_payload": row["uds_payload"],
                **classify_response(row["uds_payload"]),
            }
            for row in reader
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze synthetic UDS response payloads")
    parser.add_argument("csv_file", type=Path, help="CSV containing reassembled UDS responses")
    args = parser.parse_args()
    results = analyze_csv(args.csv_file)
    print(json.dumps(results, indent=2))
    print(f"\nSummary: {len(results)} payloads; "
          f"{sum(x['result'] == 'positive' for x in results)} positive; "
          f"{sum(x['result'] == 'negative' for x in results)} negative")


if __name__ == "__main__":
    main()
