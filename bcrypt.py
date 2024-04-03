import bcrypt

# Provided user data
users_data = [
    ('Luke', 'Skywalker', 'luke@jedi.com', 'skywalker', 'Force123', 2),
    ('Treasure', 'Hunter', 'treasurehunter@email.com', 'treasureHunter', 'XmarkstheSpot!', 1),
    ('Cyber', 'Ninja', 'cyberninja@email.com', 'cyberNinja', 'S3cur3P@ss', 1),
    ('Music', 'Maestro', 'musicmaestro@email.com', 'musicMaestro', 'Melody123$', 1),
    ('Wander', 'lust23', 'wander@email.com', 'wanderlust23', 'GlobeTrotter!', 1),
    ('Code', 'Wizard', 'codewizard@email.com', 'codeWizard', 'MagicCode$', 1),
    ('Coffee', 'Addict', 'coffee@email.com', 'coffeeAddict', 'Caf3in@te', 1),
    ('Book', 'Worm', 'bookworm@email.com', 'bookworm', 'Read1234', 1),
    ('Garden', 'Guru', 'garden@email.com', 'gardenGuru', 'Fl0w3rP0w3r!', 1),
    ('Midnight', 'Rider', 'midnight@email.com', 'midnightRider', 'N1ghtOwl&', 1)
]

# Hash passwords using bcrypt and prepare data for insertion
hashed_users_data = []
for user_data in users_data:
    firstname, lastname, email, username, password, role_id = user_data
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_users_data.append((firstname, lastname, email, username, hashed_password, role_id))

# Now, you can perform the database insertion with the hashed passwords
# Your database-specific code here (e.g., using SQLAlchemy, Django ORM, or raw SQL)

# Example of printing the modified data with hashed passwords
print(hashed_users_data)
