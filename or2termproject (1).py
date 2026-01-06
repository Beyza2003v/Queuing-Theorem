import os
import math

def display_menu():
    print("Select a Queuing Model:")
    models = [
        "1. M/M/1:GD/∞/∞",
        "2. M/M/1:GD/N/∞",
        "3. M/M/c:GD/∞/∞",
        "4. M/M/c:GD/N/∞",
        "5. M/M/∞:GD/∞/∞ (self-service model)"
    ]
    for model in models:
        print(model)

    while True:
        try:
            selected_model = int(input("Enter your choice (1-5): "))
            if selected_model in [1, 2, 3, 4, 5]:
                return selected_model
            else:
                print("Invalid choice. Please select a valid model (1 to 5).")
        except ValueError:
            print("Invalid input. Please enter a number (1 to 5).")

def ask_for_lambda_mu():
    while True:
        try:
            lambda_value = float(input("Enter λ (arrival rate): "))
            mu_value = float(input("Enter μ (service rate): "))
            
            if selected_model == 1 and lambda_value >= mu_value:
                print("Error: λ must be less than μ. Please try again.")
                continue
            
            return lambda_value, mu_value
        except ValueError:
            print("Invalid input. Please enter numeric values for λ and μ.")

def ask_for_N():
    while True:
        try:
            N = int(input("Enter N (system capacity): "))
            if N <= 0:
                print("N must be a positive integer. Please try again.")
                continue
            return N
        except ValueError:
            print("Invalid input. Please enter a positive integer for N.")
            
def ask_for_c():
    while True:
        try:
            c = int(input("Enter c (number of servers): "))
            if c <= 0:
                print("Number of servers must be greater than 0. Please try again.")
            else:
                return c
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of servers.")

def calculate_first_scenario(lambda_value, mu_value):
    print("\nCalculating for M/M/1:GD/∞/∞...")
    p0 = (mu_value - lambda_value) / mu_value

    pn_values = []
    for n in range(21):
        pn = ((lambda_value / mu_value) ** n) * p0
        pn_values.append(pn)
        print(f"p{n}: {pn:.4f}")

    lambda_eff = lambda_value
    lambda_lost = 0
    print(f"λ eff: {lambda_eff}")
    print(f"λ lost: {lambda_lost}")

    Ls = lambda_value / (mu_value - lambda_value)
    print(f"Ls: {Ls:.4f}")

    Ws = Ls / lambda_value
    print(f"Ws: {Ws:.4f}")

    Wq = Ws - (1 / mu_value)
    print(f"Wq: {Wq:.4f}")

    Lq = Wq * lambda_value
    print(f"Lq: {Lq:.4f}")

    c_bar = Ls - Lq
    print(f"c̄: {c_bar:.4f}")

def calculate_second_scenario(lambda_value, mu_value, N):
    print("\nCalculating for M/M/1:GD/N/∞...")
    
    rho = lambda_value / mu_value
    
    if rho == 1:
        p0 = 1 / (N + 1)
    else:
        p0 = (1 - rho) / (1 - rho ** (N + 1))
    print(f"p0: {p0:.4f}")

    pn_values = []
    for n in range(N + 1):
        pn = (rho ** n) * p0
        pn_values.append(pn)
        print(f"p{n}: {pn:.4f}")

    lambda_lost = lambda_value * pn_values[N]
    lambda_eff = lambda_value - lambda_lost
    print(f"λ lost: {lambda_lost:.4f}")
    print(f"λ eff: {lambda_eff:.4f}")

    numerator = (rho * (1 - (N + 1) * rho ** N + N * rho ** (N + 1)))
    denominator = (1 - rho) * (1 - rho ** (N + 1))
    Ls = numerator / denominator
    print(f"Ls: {Ls:.4f}")

    Ws = Ls / lambda_eff
    print(f"Ws: {Ws:.4f}")

    Wq = Ws - (1 / mu_value)
    print(f"Wq: {Wq:.4f}")

    Lq = Wq * lambda_eff
    print(f"Lq: {Lq:.4f}")

    c_bar = lambda_eff / mu_value
    print(f"c̄: {c_bar:.4f}")
    
def calculate_third_scenario(lambda_value, mu_value, c):
    print("\nCalculating M/M/c:GD/∞/∞ values...")
    rho = lambda_value / (c * mu_value)
    if rho >= 1:
        print("System is unstable as λ ≥ cμ.")
        return

    sum_term = sum((lambda_value / mu_value) ** n / math.factorial(n) for n in range(c))
    p0 = 1 / (sum_term + ((lambda_value / mu_value) ** c / (math.factorial(c) * (1 - rho))))

    pn_values = []
    for n in range(21):
        if n <= c:
            pn = ((lambda_value / mu_value) ** n / math.factorial(n)) * p0
        else:
            pn = ((lambda_value / mu_value) * n / (math.factorial(c) * (c * (n - c)))) * p0
        pn_values.append(pn)
        print(f"p{n}: {pn:.4f}")

    lambda_eff = lambda_value  
    lambda_lost = 0  
    print(f"λ eff: {lambda_eff:.4f}")
    print(f"λ lost: {lambda_lost:.4f}")

    numerator = ((lambda_value) ** (c + 1)) 
    denominator = ((c - lambda_value / mu_value) ** 2) * math.factorial(c - 1) * (mu_value ** (c + 1))
    Lq = (numerator / denominator) * p0
    print(f"Lq: {Lq:.4f}")

    Ls = Lq + (lambda_value / mu_value)
    print(f"Ls: {Ls:.4f}")

    Ws = Ls / lambda_eff
    print(f"Ws: {Ws:.4f}")

    Wq = Lq / lambda_eff
    print(f"Wq: {Wq:.4f}")

    c_bar = lambda_eff / mu_value
    print(f"c̄: {c_bar:.4f}")

def calculate_fourth_scenario(lambda_val, mu_val, c_val, N_val):
    rho = lambda_val / (c_val * mu_val)  

    if rho >= 1:
        print("System is unstable as λ ≥ cμ.")
        return

    sum_terms = sum(
        (lambda_val / mu_val) ** n / math.factorial(n)
        for n in range(c_val)
    )

    last_term = ((lambda_val / mu_val) ** c_val / math.factorial(c_val)) * (
        (1 - rho ** (N_val - c_val + 1)) / (1 - rho)
    )

    p0 = 1 / (sum_terms + last_term)

    pn = []
    for n in range(N_val + 1):
        if n <= c_val:
            pn_value = ((lambda_val / mu_val) ** n / math.factorial(n)) * p0
        else:
            pn_value = ((lambda_val / mu_val) ** n / (math.factorial(c_val) * (c_val ** (n - c_val)))) * p0
        pn.append(pn_value)

    lambda_lost = lambda_val * pn[N_val]
    lambda_eff = lambda_val - lambda_lost

    Ls = sum(n * pn[n] for n in range(N_val + 1))

    Lq = Ls - (lambda_eff / mu_val)

    Wq = Lq / lambda_eff
    Ws = Ls / lambda_eff
    cbar = Ls - Lq  

    print("\nResults for Scenario 4:")
    print(f"p0: {p0:.5f}")
    for i, p in enumerate(pn):
        print(f"p{i}: {p:.5f}")
    print(f"λlost: {lambda_lost:.5f}")
    print(f"λeff: {lambda_eff:.5f}")
    print(f"Ls: {Ls:.5f}")
    print(f"Lq: {Lq:.5f}")
    print(f"Ws: {Ws:.5f}")
    print(f"Wq: {Wq:.5f}")
    print(f"c̅: {cbar:.5f}")

def calculate_fifth_scenario(lambda_val, mu_val):
   
    p0 = math.exp(-lambda_val / mu_val)

    pn = []
    for n in range(21):  
        pn_value = ((lambda_val ** n) / (math.factorial(n) * (mu_val ** n))) * p0
        pn.append(pn_value)

    lambda_eff = lambda_val
    lambda_lost = 0

    Ls = lambda_val / mu_val
    Wq = 0  
    Lq = 0
    Ws = 1 / mu_val
    cbar = Ls

    print("\nResults for Scenario 5:")
    for i, p in enumerate(pn):
        print(f"p{i}: {p:.4f}")
    print(f"λeff: {lambda_eff:.4f}")
    print(f"λlost: {lambda_lost:.4f}")
    print(f"Ls: {Ls:.4f}")
    print(f"Lq: {Lq:.4f}")
    print(f"Ws: {Ws:.4f}")
    print(f"Wq: {Wq:.4f}")
    print(f"c̅: {cbar:.4f}")


    
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print("\nConsole cleared.")

def main():
    global selected_model  
    while True:
        selected_model = display_menu()

        if selected_model == 1:  
            lambda_value, mu_value = ask_for_lambda_mu()
            calculate_first_scenario(lambda_value, mu_value)
        elif selected_model == 2:  
            lambda_value, mu_value = ask_for_lambda_mu()
            N = ask_for_N()
            calculate_second_scenario(lambda_value, mu_value, N)
        elif selected_model == 3:  
            lambda_value, mu_value = ask_for_lambda_mu()
            c = ask_for_c()
            calculate_third_scenario(lambda_value, mu_value, c)
        elif selected_model == 4:  
            lambda_val, mu_val = ask_for_lambda_mu()
            c_val = ask_for_c()
            N_val = ask_for_N()
            calculate_fourth_scenario(lambda_val, mu_val, c_val, N_val)
        elif selected_model == 5:  
            lambda_val, mu_val = ask_for_lambda_mu()
            calculate_fifth_scenario(lambda_val, mu_val)

        input("\nPress Enter to clear the console and return to the menu...")  
        clear_console()

if __name__ == "__main__":
    main()