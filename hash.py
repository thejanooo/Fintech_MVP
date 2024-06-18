from streamlit_authenticator.utilities.hasher import Hasher
hashed_passwords = Hasher(['abc', 'admin']).generate()
print(hashed_passwords)