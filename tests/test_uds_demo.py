from pathlib import Path
import pytest
from uds_demo import analyze_csv, classify_response


def test_positive_read_data_by_identifier():
    result = classify_response('62 F1 90')
    assert result['result'] == 'positive'
    assert result['request_sid'] == '0x22'


def test_negative_request_out_of_range():
    result = classify_response('7F 22 31')
    assert result['result'] == 'negative'
    assert result['nrc'] == '0x31'
    assert result['description'] == 'Request Out Of Range'


def test_negative_security_access_denied():
    assert classify_response('7F 27 33')['description'] == 'Security Access Denied'


def test_empty_or_malformed_payload_is_rejected():
    for payload in ('', '7F 22', 'INVALID'):
        with pytest.raises(ValueError):
            classify_response(payload)


def test_unclassified_payload_not_misreported_as_positive():
    assert classify_response('22 F1 90')['result'] == 'unclassified'


def test_synthetic_dataset_counts():
    data = analyze_csv(Path(__file__).parent.parent / 'examples' / 'synthetic_uds_responses.csv')
    assert len(data) == 5
    assert sum(r['result'] == 'positive' for r in data) == 3
    assert sum(r['result'] == 'negative' for r in data) == 2
