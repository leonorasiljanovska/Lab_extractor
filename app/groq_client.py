#
# import json
# from openai import OpenAI
# from starlette.concurrency import run_in_threadpool
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )
#
#
# async def analyze_text_with_groq(text: str):
#     try:
#         print(f"Analyzing text: {text[:200]}...")  # Debug log
#
#         response = await run_in_threadpool(
#             client.chat.completions.create,
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system",
#                  "content": """You are a medical lab report expert. Extract test names, values, units, and reference ranges from the text.
#
# Return ONLY valid JSON in this exact format:
# {
#   "tests": [
#     {
#       "name": "Test Name",
#       "value": "Test Value",
#       "unit": "Unit",
#       "reference_range": "Reference Range",
#       "status": "Normal/High/Low"
#     }
#   ]
# }
#
# If no tests are found, return: {"tests": []}
#
# Look for patterns like:
# - "Glucose: 95 mg/dL (Normal: 70-100)"
# - "Hemoglobin 12.5 g/dL Ref: 12.0-15.5"
# - "WBC Count: 7.2 x10³/μL (4.0-11.0)"
# - Any test name followed by a number and unit
#
# Be flexible with formatting but always return valid JSON."""},
#                 {"role": "user", "content": f"Extract lab test data from this text:\n\n{text}"}
#             ],
#             temperature=0.1  # Lower temperature for more consistent output
#         )
#
#         content = response.choices[0].message.content
#         print(f"Groq response: {content}")  # Debug log
#
#         # Try to parse JSON response
#         try:
#             # Clean up the response - sometimes LLMs add extra text
#             content = content.strip()
#             if content.startswith('```json'):
#                 content = content[7:-3]  # Remove ```json and ```
#             elif content.startswith('```'):
#                 content = content[3:-3]  # Remove ``` blocks
#
#             parsed_response = json.loads(content)
#             return parsed_response
#
#         except json.JSONDecodeError as e:
#             print(f"JSON decode error: {e}")
#             print(f"Raw content: {content}")
#             # Return empty structure if JSON parsing fails
#             return {"tests": []}
#
#     except Exception as e:
#         print(f"Error in analyze_text_with_groq: {e}")
#         return {"tests": []}


import json
from openai import OpenAI
from starlette.concurrency import run_in_threadpool
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


async def analyze_text_with_groq(text: str):
    try:
        print(f"Analyzing text: {text[:200]}...")  # Debug log

        response = await run_in_threadpool(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system",
                 "content": """You are a medical lab report expert. Extract ALL information from lab reports including patient details, doctor information, clinic details, test date, and test results.

Return ONLY valid JSON in this exact format:
{
  "patient_name": "Patient Full Name",
  "gender": "Male/Female or null if not found",
  "doctor_name": "Doctor Full Name", 
  "clinic_name": "Clinic/Hospital/Laboratory Name",
  "test_date": "Date of test (any format found)",
  "report_date": "Date of report (any format found)",
  "tests": [
    {
      "name": "Test Name",
      "value": "Test Value", 
      "unit": "Unit",
      "reference_range": "Reference Range",
      "status": "Normal/High/Low"
    }
  ]
}

Look for:
- Patient name: often after "Patient:", "Name:", "Patient Name:", or at the top
- Gender: look for labels like "Gender:", "Sex:", "Sex (M/F):", or near patient name
- Doctor name: after "Dr.", "Doctor:", "Physician:", "Ordered by:", "Referring Physician:"
- Clinic/Lab: letterhead, "Laboratory:", "Clinic:", "Hospital:", facility names
- Dates: look for "Date:", "Test Date:", "Report Date:", "Collected:", any date format
- Test results: test names with values, units, and reference ranges

If any field is not found, use null for that field.
Always return valid JSON."""},
                {"role": "user", "content": f"Extract complete lab report information from this text:\n\n{text}"}
            ],
            temperature=0.1  # Lower temperature for more consistent output
        )

        content = response.choices[0].message.content
        print(f"Groq response: {content}")  # Debug log

        # Try to parse JSON response
        try:
            # Clean up the response - sometimes LLMs add extra text
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:-3]  # Remove ```json and ```
            elif content.startswith('```'):
                content = content[3:-3]  # Remove ``` blocks

            parsed_response = json.loads(content)
            return parsed_response

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw content: {content}")
            # Return empty structure if JSON parsing fails
            return {
                "patient_name": None,
                "doctor_name": None,
                "clinic_name": None,
                "test_date": None,
                "report_date": None,
                "tests": []
            }

    except Exception as e:
        print(f"Error in analyze_text_with_groq: {e}")
        return {
            "patient_name": None,
            "doctor_name": None,
            "clinic_name": None,
            "test_date": None,
            "report_date": None,
            "tests": []
        }