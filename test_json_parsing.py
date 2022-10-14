import json
import pytest
from console_utility import Parser


@pytest.mark.parametrize("json_input, parsed_json", [
    ('./data/schema.json', '{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', '
                           '\'government\']", "age": "int:rand(1, 90)"}'),
    ('{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', \'government\']", '
     '"age": "int:rand(1, 90)"}',
     '{"date":"timestamp:", "name": "str:rand", "type":"[\'client\', \'partner\', \'government\']", '
     '"age": "int:rand(1, 90)"}')
])
def test_schema_deserialization(json_input, parsed_json):
    parser = Parser()
    result = parser.schema_deserialization(json_input)
    actual = json.loads(parsed_json)
    assert actual == result
