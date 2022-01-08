def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        print(text)

if __name__ == '__main__':
    main()
