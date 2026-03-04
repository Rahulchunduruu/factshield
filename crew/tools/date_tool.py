from crewai.tools import BaseTool
from dateutil import parser
from datetime import datetime
from pydantic import BaseModel
from typing import Type

class DateInput(BaseModel):
    date_text: str

class DateValidatorTool(BaseTool):
    name: str = "Date Validator"
    description: str = "Extracts and validates dates from text to check if claims are about future/past events"
    args_schema: Type[DateInput] = DateInput

    def _run(self, date_text: str) -> dict:
        try:
            parsed_date = parser.parse(date_text, fuzzy=True)
            now = datetime.now()
            
            return {
                "parsed_date": str(parsed_date),
                "is_future": parsed_date > now,
                "is_past": parsed_date < now,
                "days_difference": (parsed_date - now).days
            }
        except Exception as e:
            return {"error": str(e)}

date_validator_tool = DateValidatorTool()


if __name__ == "__main__":

# Test with your claim
    result = date_validator_tool._run("early 2026")
# Returns: {'parsed_date': '2026-01-01', 'is_future': True, 'days_difference': 400+}
    print(result)

