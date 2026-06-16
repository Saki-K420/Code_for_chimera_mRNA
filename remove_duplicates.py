import sys

def remove_duplicate_lines_ignore_col4(input_file, output_file):
    try:
        seen = set()
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                columns = line.strip().split('\t')

                # 4列目を無視して識別キーを作成
                if len(columns) >= 5:  # 少なくとも5列以上あることを確認
                    key = tuple(columns[:3] + columns[4:])  # 1-3列目 + 5列目以降を使用
                else:
                    key = tuple(columns)  # 5列未満ならそのまま比較

                if key not in seen:
                    seen.add(key)
                    outfile.write(line)

        print(f"Processing complete. Unique lines written to {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_duplicates.py input.bed output.bed")
        sys.exit(1)

    remove_duplicate_lines_ignore_col4(sys.argv[1], sys.argv[2])
