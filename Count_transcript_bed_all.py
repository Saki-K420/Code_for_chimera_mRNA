import pandas as pd
import sys

def count_repeatname_lines_with_class(bed_file, output_csv=None):
    try:
        bed_df = pd.read_csv(bed_file, sep='\t', header=None, dtype=str)

        repeatname_col = 9   # column [10]
        class_col = 12       # column [13]
        subclass_col = 13    # column [14]

        required_cols = max(repeatname_col, class_col, subclass_col)
        if required_cols >= len(bed_df.columns):
            print(f"Error: The BED file does not contain the necessary columns (repeatname: 10, class: 13, subclass: 14).")
            sys.exit(1)

        # Remove `NaN` from column `repeatname`
        bed_df = bed_df.dropna(subset=[repeatname_col])

        # Count each repeatname
        repeatname_counts = bed_df[repeatname_col].value_counts().reset_index()
        repeatname_counts.columns = ["repeatname", "Number of lines"]

        # Get the class and subclass associated with each repeat name.
        class_info = bed_df.groupby(repeatname_col).first()[[class_col, subclass_col]].reset_index()
        class_info.columns = ["repeatname", "class", "subclass"]

        # Merge repeatname classes and counts
        result_df = pd.merge(repeatname_counts, class_info, on="repeatname", how="left")

        print(result_df.to_string(index=False))

        # Output as CSV file
        if output_csv:
            result_df.to_csv(output_csv, index=False)
            print(f"\nResults saved to {output_csv}")

    except Exception as e:
        print(f"Error processing {bed_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <bed_file> [output_csv]")
        sys.exit(1)

    bed_file = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) == 3 else None

    count_repeatname_lines_with_class(bed_file, output_csv)
