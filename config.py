class Config:
    def __init__(self):
        self.pu = load_p_users()
    
    def load_p_users(self):
        with open("configs/p_users.txt") as f:
            self.pu = f.read().split('\n')
        return pu

    def save_p_users(self):
        with open("configs/p_users.txt") as f:
            f.write("\n".join(self.pu))
        return