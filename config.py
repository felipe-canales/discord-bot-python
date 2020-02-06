class Config:
    def __init__(self):
        self.pu = self.load_p_users()
    
    def load_p_users(self):
        with open("configs/p_users.txt") as f:
            pu = f.read().split('\n')
        return pu

    def save_p_users(self):
        with open("configs/p_users.txt", "w") as f:
            f.write("\n".join(self.pu))
        return

    def add_p_user(self, id):
        if not id in self.pu:
            self.pu.append(str(id))
            return True
        return False

    def remove_p_user(self, id):
        if id in self.pu:
            self.pu.remove(str(id))
            return True
        return False

    def check_p_user(self, id):
        return str(id) in self.pu