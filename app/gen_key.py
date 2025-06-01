import secrets
JWT_SECRET_KEY = secrets.token_urlsafe(32)

# Save the key to a .env file
with open('G:\srimanta\Gen AI\DataBricks\Flask HandsOn\proj-ap-demo\proj-apl-0101-demo\.env', 'a') as env_file:
    env_file.write(f'JWT_SECRET_KEY={JWT_SECRET_KEY}\n')
