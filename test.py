import requests

settings = {
    'SM_API_KEY': '3C3D892A3F', 
    'SM_URL': 'https://www.reddit.com/r/whatisthisthing/comments/9ixdh9/found_hooked_up_to_my_router/e6nh61r/',
    'SM_LENGTH': '4'
    }


request = requests.post("https://api.smmry.com", params=settings)

print(request.url)
print(request.json())
