import sys
from utils.prompts import *
from utils.exception import BlogException

def content_generation(client, SYSTEM_TEMPLATE, USER_TEMPLATE):
    try:
        response=client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": SYSTEM_TEMPLATE},
                {"role": "user", "content": USER_TEMPLATE}
            ],
            temperature=1,
            response_format={'type':'json_object'}
            )
        data = response.choices[0].message.content

        return data
    except Exception as e:
        raise BlogException(e,sys)
