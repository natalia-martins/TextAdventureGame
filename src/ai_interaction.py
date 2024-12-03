from openai import OpenAI

client = OpenAI()


def ai_request(input_array):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=input_array
    )

    return completion.choices[0].message
