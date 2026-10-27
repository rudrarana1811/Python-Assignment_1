from collections import deque
import re


class Node:
    def __init__(self):
        self.next = {}
        self.fail = 0
        self.output = False


def build_automaton(words):
    nodes = [Node()]

    for word in words:
        current = 0

        for char in word.lower():
            if char not in nodes[current].next:
                nodes[current].next[char] = len(nodes)
                nodes.append(Node())

            current = nodes[current].next[char]

        nodes[current].output = True

    queue = deque()

    for child in nodes[0].next.values():
        queue.append(child)
    # Build failure links for the automaton

    while queue:
        current = queue.popleft()

        for char, child in nodes[current].next.items():
            queue.append(child)

            failure = nodes[current].fail

            while failure and char not in nodes[failure].next:
                failure = nodes[failure].fail

            if char in nodes[failure].next:
                nodes[child].fail = nodes[failure].next[char]

            if nodes[nodes[child].fail].output:
                nodes[child].output = True

    return nodes


def contains_banned_word(password, nodes):
    current = 0
# Search the password using the automaton
    for char in password.lower():
        while current and char not in nodes[current].next:
            current = nodes[current].fail

        if char in nodes[current].next:
            current = nodes[current].next[char]
        else:
            current = 0

        if nodes[current].output:
            return True

    return False


def classify_password(password, nodes):
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    if contains_banned_word(password, nodes):
        return "COMPROMISED"

    if re.search(r"(.)\1\1\1", password):
        return "WEAK_PATTERN"

    if not re.search(r"[a-z]", password):
        return "WEAK_PATTERN"

    if not re.search(r"[A-Z]", password):
        return "WEAK_PATTERN"

    if not re.search(r"\d", password):
        return "WEAK_PATTERN"

    if not re.search(r"[$#@]", password):
        return "WEAK_PATTERN"

    return "STRONG"


print("Optimized Password Audit")
print("Enter number of banned words:")
b = int(input())

if not 1 <= b <= 10000:
    print("Invalid input")
    raise SystemExit

banned_words = []

print("Enter banned words:")

for i in range(b):
    print(f"Banned word {i + 1}:")
    banned_words.append(input().strip())

nodes = build_automaton(banned_words)

print("Enter number of passwords:")
n = int(input())

if not 1 <= n <= 100000:
    print("Invalid input")
    raise SystemExit

print("Enter passwords:")

for index in range(1, n + 1):
    print(f"Password {index}:")
    password = input().rstrip("\n")

    print(f"{index}: {classify_password(password, nodes)}")
