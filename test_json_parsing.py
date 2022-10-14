import json
import pytest
from main import schema_deserialization


@pytest.mark.parametrize("json_input, parsed_json", [
    ('./data/schema.json', '{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', '
                           '\'government\']", "age": "int:rand(1, 90)"}'),
    ('{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', \'government\']", '
     '"age": "int:rand(1, 90)"}',
     '{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', \'government\']", '
     '"age": "int:rand(1, 90)"}')
])
def test_schema_deserialization(json_input, parsed_json):
    result = schema_deserialization(json_input)
    actual = json.loads(parsed_json)
    assert actual == result
