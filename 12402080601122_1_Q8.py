import os
import re
import pickle
import zipfile


def build_index(folder):
    index = {}
    total_files = 0
    total_lines = 0

    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        if not filename.lower().endswith(".txt"):
            continue

        total_files += 1

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            for line_number, line in enumerate(file, 1):
                total_lines += 1

                words = re.findall(
                    r"[A-Za-z0-9_]+",
                    line.lower()
                )

                for word in words:
                    if word not in index:
                        index[word] = []

                    index[word].append(
                        (filename, line_number)
                    )

    return index, total_files, total_lines


print("Compressed Log Index")
print("Enter mode (BUILD or SEARCH):")
first_line = input().strip()

parts = first_line.split()

if parts[0].upper() == "BUILD":
    if len(parts) == 3:
        folder = parts[1]
        archive = parts[2]
    else:
        print("Enter logs folder path:")
        folder = input().strip()

        print("Enter output zip file name:")
        archive = input().strip()

    if not os.path.isdir(folder):
        print("Folder not found")
        raise SystemExit

    index, total_files, total_lines = build_index(folder)

    with open("index.pkl", "wb") as file:
        pickle.dump(index, file)

    with zipfile.ZipFile(
        archive,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:
# Read each text file and store token positions
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)

            if os.path.isfile(path):
                zip_file.write(
                    path,
                    os.path.join("logs", filename)
                )

        zip_file.write("index.pkl")

    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")

elif parts[0].upper() == "SEARCH":
    if len(parts) == 2:
        pickle_file = parts[1]
    else:
        print("Enter pickle file path:")
        pickle_file = input().strip()

    print("Enter number of search tokens:")
    q = int(input())

    with open(pickle_file, "rb") as file:
        index = pickle.load(file)

    print("Enter search tokens:")

    for i in range(q):
        print(f"Token {i + 1}:")
        token = input().strip().lower()

        for filename, line_number in index.get(token, []):
            print(f"{filename}:{line_number}")

else:
    print("Invalid mode")
