def get_contract():
    with open("log.txt", "r+") as file:
        first_line = file.readline()
        if first_line:
            print("Contract Addess:", first_line.strip().split(" ")[5])
            print("RPC URL        : https://eth-sepolia.g.alchemy.com/v2/SMfUKiFXRNaIsjRSccFuYCq8Q3QJgks8")
            print("To start       : Read the given source, figure it out what to do from here.")
            print("")
            print("Note: Due it's deployed on Sepolia network, please use your own Private key to do the transaction")
            print("      If you need funds, you can either DM the probset or get it on https://sepoliafaucet.com/")
            file.seek(0)
            remaining_lines = file.readlines()
            remaining_lines = remaining_lines[1:]
            file.seek(0)
            file.truncate()
            file.writelines(remaining_lines)
            for line in remaining_lines:
                line.strip()
        else:
            print("No contract addresses found in the file.")

def how():
    print("Ga ada how2nya sih, paling, semangat gan kerjainnya :D")

def main():
    print("Welcome to TCP1P Blockchain Bootcamp")
    print("")
    print("1. How to 101?")
    print("2. get Contract")
    option = int(input(">> "))
    if option == 1:
        how()
        exit()
    elif option == 2:
        get_contract()
    else:
        print("Invalid Input!")

if __name__ == "__main__":
    main()
