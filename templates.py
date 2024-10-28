OPENAI_MASK = "{text}"
OPENAI_MESSAGES = [
  {
    "role": "system",
    "content": "You are an expert English linguist."
  },
  {
    "role": "user", "content": "Find 5 ways to rephrase the following phrase: {text}. "
                               "Format answers as a bulleted list."
  }
]
