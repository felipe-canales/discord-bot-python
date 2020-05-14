class Config:
    # Saves user permissions.
    # A user is a line in the format "id,perms"
    # permissions are specified with letters:
    # - a: operate all servers
    # - v: operate vanilla server
    # - b: operate bedrock server
    # - o: give or take permission of other users

    def __init__(self):
        self.pu, self.users = self.load_p_users()
    
    def load_p_users(self):
        with open("configs/p_users.txt") as f:
            pu = [pair.split(',') for pair in f.read().split('\n')]
        return pu, [pair[0] for pair in pu]

    def save_p_users(self):
        with open("configs/p_users.txt", "w") as f:
            users = [",".join(pair) for pair in self.pu]
            f.write("\n".join(users))
        return

    def add_p_user(self, id, perms):
        if not id in self.users:
            self.pu.append((id, perms))
            return True
        return False

    def edit_p_user(self, id, perms):
        return self.remove_p_user(id) and self.add_p_user(id,perms)

    def remove_p_user(self, id):
        if id in self.users:
            self.users.remove(id)
            for pair in self.pu:
                if pair[0] == id:
                    self.pu.remove(pair)
                    break
            return True
        return False

    def check_p_user(self, id, perm):
        if id not in self.users:
            return False
        for pair in self.pu:
            if pair[0] == id:
                return perm in pair[1]
    
    def get_p_user(self, id):
        if id not in self.users:
            return ""
        for pair in self.pu:
            if pair[0] == id:
                return pair[1]
    