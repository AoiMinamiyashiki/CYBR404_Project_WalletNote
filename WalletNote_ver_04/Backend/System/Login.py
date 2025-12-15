import hashlib
from WalletNote_ver_04.Backend.Database.ConnectDatabase import ConnectDatabase

class Login(ConnectDatabase):
    def authenticate(self, email, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute(
            "SELECT id, username FROM users WHERE email=%s AND password=%s",
            (email, hashed)
        )
        return self.cursor.fetchone()
