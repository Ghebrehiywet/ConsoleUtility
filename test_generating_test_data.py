import pytest
from console_utility import generating_test_data


@pytest.mark.parametrize("key, value, result_len", [
    # ('date', 'timestamp:', 18),
    ('name', 'str:rand', 36),
])
def test_generating_test_data(key, value, result_len):
    generated_test_data = generating_test_data(key, value)
    assert len(str(generated_test_data)) == result_len


@pytest.mark.parametrize("key, value, result", [
    ('name', 'str:', ''),
    ('age', 'int:', None),
])
def test_empty_value_to_generate_test_data(key, value, result):
    generated_test_data = generating_test_data(key, value)
    assert generated_test_data == result


@pytest.mark.parametrize("key, value, result", [
    ('name', 'str:cat', 'cat'),
    ('age', 'int:38', '38'),
])
def test_standalone_value_to_generate_test_data(key, value, result):
    generated_test_data = generating_test_data(key, value)
    assert generated_test_data == result


@pytest.mark.parametrize("key, value, error_value", [
    ('name', 'str:123', '1'),
    ('age', 'int:head', '1'),
])
def test_invalid_standalone_value_to_generate_test_data(key, value, error_value):
    with pytest.raises(SystemExit) as exc_info:
        generated_test_data = generating_test_data(key, value)
    assert str(exc_info.value) == error_value


@pytest.mark.parametrize("key, value, _from, _to", [
    ('name', 'int:rand(1,100)', 1, 100),
    ('age', 'int:rand(100, 200)', 100, 200),
])
def test_ranged_rand_value_to_generate_test_data(key, value, _from, _to):
    generated_test_data = generating_test_data(key, value)
    assert _from <= int(generated_test_data) < _to


@pytest.mark.parametrize("key, value, error_value", [
    ('name', 'str:rand(1, 100)', '1'),
])
def test_invalid_str_ranged_rand_value_to_generate_test_data(key, value, error_value):
    with pytest.raises(SystemExit) as exc_info:
        generated_test_data = generating_test_data(key, value)
    assert str(exc_info.value) == error_value


@pytest.mark.parametrize("key, value, choices", [
    ('type_option_one', "str:['client', 'partner', 'government']", {'client', 'partner', 'government'}),
    ('type_option_two', "['client', 'partner', 'government']", {'client', 'partner', 'government'}),
    ('age_option_one', "int:[0, 9, 10, 4]", {0, 9, 10, 4}),
    ('age_option_two', "[0, 9, 10, 4]", {0, 9, 10, 4}),
])
def test_lists_rand_value_to_generate_test_data(key, value, choices):
    generated_test_data = generating_test_data(key, value)
    assert generated_test_data in choices

