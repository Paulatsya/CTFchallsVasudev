#!/usr/bin/env python3
import sys
import random
import threading
import queue
import time

FLAG = "dscctf{7rU7h_15_5ubj3c7iv3}"
TIMEOUT = 10  # seconds per question

def input_with_timeout(prompt, timeout):
    """Prompt the user and wait for input with a timeout using a background thread."""
    print(prompt, end='', flush=True)
    q = queue.Queue()

    def worker():
        try:
            q.put(input())
        except Exception:
            q.put(None)

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    try:
        return q.get(timeout=timeout)
    except queue.Empty:
        return None

def main():
    print("Welcome to the Dystopian Arithmetic Challenge!")
    print("In our society, truth is subjective. For example, we declare that 2+2 equals 5.")
    if input("Do you accept this new truth? (yes/no) ").strip().lower() != "yes":
        print("Access denied!")
        return

    print("\nThe rules here are not as you know them. Answer the following questions within 10 seconds each!")
    
    rounds = []
    even_found = False
    odd_found = False

    # Generate 5 rounds of arithmetic challenges.
    for _ in range(5):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-", "*"])
        expr = f"{a} {op} {b}"
        try:
            standard = eval(expr)
        except Exception:
            standard = 0
        # Hidden transformation rule:
        # If the normal result is even, the correct answer is standard + 1.
        # If the normal result is odd, the correct answer is standard - 1.
        if standard % 2 == 0:
            expected = standard + 1
            even_found = True
        else:
            expected = standard - 1
            odd_found = True
        rounds.append((expr, expected))

    # Ensure at least one round yields an even standard result and one an odd result.
    if not even_found:
        while True:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(["+", "-", "*"])
            expr = f"{a} {op} {b}"
            standard = eval(expr)
            if standard % 2 == 0:
                rounds[0] = (expr, standard + 1)
                break
    elif not odd_found:
        while True:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(["+", "-", "*"])
            expr = f"{a} {op} {b}"
            standard = eval(expr)
            if standard % 2 != 0:
                rounds[0] = (expr, standard - 1)
                break

    # Run through the rounds.
    for i, (expr, expected) in enumerate(rounds, start=1):
        answer = input_with_timeout(f"\nRound {i}: What is {expr}? ", TIMEOUT)
        if answer is None:
            print("\nTime's up! You took too long to answer.")
            return
        try:
            if int(answer.strip()) != expected:
                print("Incorrect! You have failed to embrace our altered arithmetic.")
                return
            else:
                print("Correct!")
        except:
            print("Invalid input!")
            return

    print("\nCongratulations! You have mastered our new truth!")
    print("Here is your flag:")
    print(FLAG)

if __name__ == "__main__":
    main()
