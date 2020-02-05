def load_p_users():
    with open("configs/p_users.txt") as f:
        pu = f.read().split('\n')
    return pu

def save_p_users(pu_list):
    with open("configs/p_users.txt") as f:
        f.write("\n".join(pu_list))
    return