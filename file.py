import msvcrt

def get_key():
    key = msvcrt.getch()
    if key == b'\r':
        return "Enter"
    elif key == b'\x08':  # Detection de la touche de suppression (Backspace)
        return "Back"
    else:
        return key.decode()

print(get_key())