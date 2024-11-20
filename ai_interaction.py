from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a very descriptive narrator."
        },
        {
            "role": "user",
            "content": "Write the start of a medieval adventure with a lone main character."
        }
    ]
)

print(completion.choices[0].message)
