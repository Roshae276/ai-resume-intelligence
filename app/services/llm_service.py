from pathlib import Path
import json

from openai import OpenAI

from app.core.settings import settings
from app.schemas.resume_parser_schema import ResumeParserResponse
from app.schemas.job_schema import JobResponse
from app.schemas.ats_schema import ATSResponse


class LLMService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def load_prompt(
        self,
        prompt_name: str
    ):

        prompt_path = Path(
            f"app/prompts/{prompt_name}"
        )

        return prompt_path.read_text(
            encoding="utf-8"
        )

    def parse_resume(
        self,
        resume_text: str
    ):

        prompt = self.load_prompt(
        "resume_parser.txt"
    )

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": resume_text,
                },
            ],
            text_format=ResumeParserResponse,
        )
        
        return response.output_parsed
    
    def parse_job_description(
        self,
        job_text: str
    ):

        prompt = self.load_prompt(
            "job_parser.txt"
        )

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": job_text,
                },
            ],
            text_format=JobResponse,
        )

        return response.output_parsed
    
    def generate_ats_report(
        self,
        resume: dict,
        job: dict
    ):

        prompt = self.load_prompt(
            "ats_prompt.txt"
        )

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": (
                        "Resume:\n"
                        + json.dumps(resume, indent=2)
                        + "\n\nJob Description:\n"
                        + json.dumps(job, indent=2)
                    ),
                },
            ],
            text_format=ATSResponse,
        )

        return response.output_parsed