import openai

OPENAI_KEY = 'YOUR OPENAI KEY'

class OpenaiService:
    def __init__(self):
        openai.api_key = OPENAI_KEY
        pass

    def job_proposal(self, project_details, skills_prompt):
        prompt_proposal = f"Generate a proposal for this freelance job titled '{project_details}' based on my skills. I have experience in  {skills_prompt}."
        try:
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                    {"role": "system", "content": "You are an assistant specialized in writing freelance proposals. When given a job title and the user's skills, generate a concise and convincing proposal."},
                    {"role": "user", "content": prompt_proposal}
                ],
            temperature=0.5,
            max_tokens=100
            )
            article_summary = response['choices'][0]['message']['content'].strip()
            article_summary = article_summary.replace('Subject: ', '')
            print(article_summary)
            return article_summary
        except Exception as e:
            print(f"Error al llamar a la API de OpenAI y traducir el Titulo: {e}")
