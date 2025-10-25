import schemathesis
from schemathesis.specs.openapi.schemas import BaseOpenAPISchema

schema: BaseOpenAPISchema = schemathesis.openapi.from_url(
    "http://localhost:8000/openapi.json"
)


@schema.parametrize()
def test_api(case) -> None:
    # Automatically calls your API and validates the response
    case.call_and_validate()
