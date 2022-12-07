from pynput.keyboard import Controller, KeyCode


def main():
    keyboard = Controller()

    keyboard.press(KeyCode.from_vk(0xB2)) #Stop key

    # 0xB2 # Next Track
    # 0xB1 # Previous Track
    # 0xB2 # Stop Media
    # 0xB3 # Play/Pause Key
    # 0xFA # Play Key ~ Does not seem to work

if __name__ == "__main__":
    main()