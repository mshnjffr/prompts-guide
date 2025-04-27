from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.completions = os.getenv('CODY_COMPLETIONS_ENDPOINT')
        self.sg_token = os.getenv('ACCESS_TOKEN')
        self.model = os.getenv('model')
        self.x_requested_with = os.getenv('X-Requested-With')

    def validate(self):
        required = ['completions', 'sg_token', 'x_requested_with']
        missing = [attr for attr in required if not getattr(self, attr)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
