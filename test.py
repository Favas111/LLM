import requests

url = "http://localhost:10000/"
email_content = """
Dear Jason,
I hope this message finds you well. I'm Shirley from Gucci;

I'm looking to purchase some company T-shirts for my team. We are a team of 100k people, and we want to get 2 T-shirts per person.

Please let me know the price and timeline you can work with.

Looking forward,
Shirley Lou
"""

payload = {"from_email": "jason@example.com", "content": email_content}
response = requests.post(url, json=payload)

if response.status_code == 200:
    extracted_info = response.json()
    print(extracted_info)
else:
    print("Error:", response.status_code, response.text)
