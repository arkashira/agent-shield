# main.py

from role_manager import RoleManager

def get_role_manager():
    return RoleManager()

def main():
    role_manager = get_role_manager()
    # Example usage of role_manager
    role_manager.assign_role("user1", "admin")
    print(role_manager.check_role("user1", "admin"))  # Should print True

if __name__ == "__main__":
    main()