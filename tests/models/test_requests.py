import pytest

from crawler_api.models.requests import LegalProcess


@pytest.mark.parametrize(
    'value',
    (
        '1234',
        '1234567-000-1234.00.00',
        '1234567-12.1234.1.12.12345'
    )
)
def test_legal_process_number_field_regex_validation(value):
    with pytest.raises(ValueError) as error:
        LegalProcess(number=value)
    assert error.value.errors() == [
        {
            'loc': ('number',),
            'msg': 'Invalid number format. Example: 1234567-12.1234.1.12.1234',
            'type': 'value_error'
        }
    ]
    assert error.value.model == LegalProcess


def test_legal_process_creation():
    legal_process = LegalProcess(number='1234567-12.1234.1.12.1234')
    assert legal_process.number == '1234567-12.1234.1.12.1234'


def test_legal_process_number_field_description():
    assert LegalProcess.__fields__['number'].field_info.description == 'Valid format: XXXXXXXX-XX-XXXX.XX.XXXX'


def test_legal_process_number_field_example():
    assert LegalProcess.__fields__['number'].field_info.extra['example'] == '1234567-12.1234.1.12.1234'
