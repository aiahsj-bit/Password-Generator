import random
import string
import os

# ── Character sets ─────────────────────────────────────────────────────────────
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS    = string.digits
SYMBOLS   = "!@#$%^&*()-_=+[]{}|;:,.<>?"

FILENAME  = "saved_passwords.txt"

# ══════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATORS
# ══════════════════════════════════════════════════════════════════════════════

def get_valid_length():
    """Ask the user for a password length and validate it."""
    while True:
        try:
            length = int(input("  Enter password length (8-64): "))
            if 8 <= length <= 64:
                return length
            else:
                print("    ❌ Please enter a number between 8 and 64.\n")
        except ValueError:
            print("    ❌ That's not a valid number. Try again.\n")


def get_yes_no(prompt):
    """Ask a yes/no question and validate the answer."""
    while True:
        answer = input(f"  {prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("    ❌ Please type 'y' or 'n'.\n")


def get_identifier():
    """Ask for an email or username and validate it."""
    while True:
        value = input("  Email or username: ").strip()
        if len(value) == 0:
            print("    ❌ Cannot be empty.\n")
        elif len(value) < 3:
            print("    ❌ Too short. At least 3 characters.\n")
        elif "@" in value and "." not in value.split("@")[-1]:
            print("    ❌ Email looks invalid (e.g. missing .com). Try again.\n")
        else:
            return value


def get_website():
    """Ask for a website name and validate it."""
    while True:
        value = input("  Website (e.g. github.com): ").strip()
        if len(value) == 0:
            print("    ❌ Cannot be empty.\n")
        elif " " in value:
            print("    ❌ No spaces allowed in a website name.\n")
        elif len(value) < 3:
            print("    ❌ Too short.\n")
        else:
            if not value.startswith("http"):
                value = "https://" + value
            return value


# ══════════════════════════════════════════════════════════════════════════════
# STRENGTH CHECKER
# ══════════════════════════════════════════════════════════════════════════════

def check_strength(password):
    """Score the password and return a strength label."""
    score = 0
    if len(password) >= 12:                         score += 1
    if len(password) >= 16:                         score += 1
    if any(c.isupper()    for c in password):       score += 1
    if any(c.islower()    for c in password):       score += 1
    if any(c.isdigit()    for c in password):       score += 1
    if any(c in SYMBOLS   for c in password):       score += 1

    if score <= 2:   return "❌ Weak"
    elif score <= 4: return "⚠️  Fair"
    elif score == 5: return "✅ Strong"
    else:            return "🔒 Very Strong"


# ══════════════════════════════════════════════════════════════════════════════
# PASSWORD GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Build a random password, guaranteeing at least one char from each chosen type."""
    charset  = ""
    required = []

    if use_upper:
        charset += UPPERCASE
        required.append(random.choice(UPPERCASE))
    if use_lower:
        charset += LOWERCASE
        required.append(random.choice(LOWERCASE))
    if use_digits:
        charset += DIGITS
        required.append(random.choice(DIGITS))
    if use_symbols:
        charset += SYMBOLS
        required.append(random.choice(SYMBOLS))

    if not charset:
        print("\n    ❌ You must select at least one character type!\n")
        return None

    remaining     = [random.choice(charset) for _ in range(length - len(required))]
    password_list = required + remaining
    random.shuffle(password_list)
    return "".join(password_list)


# ══════════════════════════════════════════════════════════════════════════════
# FILE OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

def save_entry(password):
    """Ask for account details and save everything to the file."""
    print("\n  ── Enter details for this password ──")
    identifier = get_identifier()
    website    = get_website()
    strength   = check_strength(password)

    entry = (
        f"Website  : {website}\n"
        f"Username : {identifier}\n"
        f"Password : {password}\n"
        f"Strength : {strength}\n"
        f"{'-' * 45}\n"
    )

    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"\n  ✅ Entry saved to '{FILENAME}'")


def view_saved():
    """Print all saved entries from the file."""
    if not os.path.exists(FILENAME):
        print("\n  📂 No saved entries yet.\n")
        return

    with open(FILENAME, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("\n  📂 The file is empty.\n")
        return

    print(f"\n{'=' * 45}")
    print("          📋 Saved Entries")
    print(f"{'=' * 45}\n")
    print(content)
    print(f"\n{'=' * 45}\n")


def delete_entry():
    """Show all entries numbered and let the user delete one by number."""
    if not os.path.exists(FILENAME):
        print("\n  📂 No saved entries yet.\n")
        return

    with open(FILENAME, "r", encoding="utf-8") as f:
        content = f.read()

    # Each entry ends with the dashed separator line
    entries = [e.strip() for e in content.split("-" * 45) if e.strip()]

    if not entries:
        print("\n  📂 No entries to delete.\n")
        return

    print(f"\n{'=' * 45}")
    print("       🗑️  Delete an Entry")
    print(f"{'=' * 45}\n")
    for i, entry in enumerate(entries, 1):
        first_line = entry.split("\n")[0]   # show just the Website line
        print(f"  [{i}] {first_line}")

    print()
    while True:
        try:
            choice = int(input(f"  Enter number to delete (1-{len(entries)}): "))
            if 1 <= choice <= len(entries):
                removed = entries.pop(choice - 1)
                website_line = removed.split("\n")[0]
                # Rewrite file without the deleted entry
                with open(FILENAME, "w", encoding="utf-8") as f:
                    for entry in entries:
                        f.write(entry + "\n" + "-" * 45 + "\n")
                print(f"\n  ✅ Deleted: {website_line}\n")
                break
            else:
                print(f"    ❌ Enter a number between 1 and {len(entries)}.\n")
        except ValueError:
            print("    ❌ That's not a valid number.\n")


# ══════════════════════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════════════════════
def print_menu():
    print(f"\n{'=' * 45}")
    print("       🔐 Password Generator v1.1")
    print(f"{'=' * 45}")
    print("  [1] Generate a new password")
    print("  [2] View saved entries")
    print("  [3] Delete an entry")
    print("  [4] Exit")
    print(f"{'=' * 45}")


def get_menu_choice():
    while True:
        choice = input("  Choose an option (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("    ❌ Please enter 1, 2, 3, or 4.\n")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    while True:
        print_menu()
        choice = get_menu_choice()

        # ── Generate ──────────────────────────────────────
        if choice == "1":
            print(f"\n{'─' * 45}")
            length = get_valid_length()

            print("\n  Choose character types:")
            use_upper   = get_yes_no("Uppercase letters (A-Z)?")
            use_lower   = get_yes_no("Lowercase letters (a-z)?")
            use_digits  = get_yes_no("Numbers (0-9)?")
            use_symbols = get_yes_no("Symbols (!@#$...)?")

            password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)

            if password:
                strength = check_strength(password)
                print(f"\n  {'─' * 41}")
                print(f"  Generated : {password}")
                print(f"  Strength  : {strength}")
                print(f"  {'─' * 41}\n")

                if get_yes_no("Save this password?"):
                    save_entry(password)

        # ── View ──────────────────────────────────────────
        elif choice == "2":
            view_saved()

        # ── Delete ────────────────────────────────────────
        elif choice == "3":
            delete_entry()

        # ── Exit ──────────────────────────────────────────
        elif choice == "4":
            print("\n  Goodbye! Stay safe. 🔒\n")
            break


if __name__ == "__main__":
    main()


    #hey How R U??