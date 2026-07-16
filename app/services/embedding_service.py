from openai import OpenAI

from app.core.settings import settings


class EmbeddingService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def create_embedding(
        self,
        text: str
    ):

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding
    
    
    def build_resume_document(
        self,
        resume: dict
    ):

        skills = "\n".join(
            resume.get("skills", [])
        )

        education = "\n".join(
            item["degree"]
            for item in resume.get(
                "education",
                []
            )
        )

        projects = "\n".join(
            item["title"]
            for item in resume.get(
                "projects",
                []
            )
        )

        text = f"""
    Name:
    {resume.get("name")}

    Skills:
    {skills}

    Education:
    {education}

    Projects:
    {projects}
    """

        return text
    
    def build_job_document(
        self,
        job: dict
    ):

        skills = "\n".join(
            job.get("skills", [])
        )

        responsibilities = "\n".join(
            job.get("responsibilities", [])
        )

        return f"""
    Job Title:
    {job.get("job_title")}

    Skills:
    {skills}

    Experience:
    {job.get("experience")}

    Education:
    {job.get("education")}

    Responsibilities:
    {responsibilities}
    """