import hashlib
from WalletNote_ver_04.Backend.Database.SaveDatabase import SaveDatabase
from WalletNote_ver_04.Backend.Information.InputUserInformation import InputUserInformation

class Signup:
    def register(self, user: InputUserInformation):
        hashed = hashlib.sha256(user.password.encode()).hexdigest()
        SaveDatabase().save_user(user.username, user.email, hashed)
