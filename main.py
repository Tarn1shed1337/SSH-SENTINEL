import sys
import sentinel_hardener
import sentinel_watcher
import pyfiglet



def main():
    title = pyfiglet.figlet_format("SSH Sentinel", font="slant")
    print(title)
    print("By Chemseddin \n")
    print("1. Audit & Harden System (One-time)")
    print("2. Start Active Defense Watcher (Persistent)")
    print("3. Exit")
    
    choice = input("\nSelect an option: ")

    if choice == '1':
        r = sentinel_hardener.run_audit()
        if r and input("Apply fixes? (y/n): ").lower() == 'y':
            sentinel_hardener.apply_fixes()
    elif choice == '2':
        try:
            sentinel_watcher.watch_logs()
        except KeyboardInterrupt:
            print("\n Watcher stopped.")
    else:
        sys.exit()

if __name__ == "__main__":
    main()