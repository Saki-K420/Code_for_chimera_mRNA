import pandas as pd
import sys

def count_repeatname_lines_with_class(bed_file, output_csv=None):
    try:
        # BEDファイルを読み込み（タブ区切り）
        bed_df = pd.read_csv(bed_file, sep='\t', header=None, dtype=str)

        # 各列のインデックス
        repeatname_col = 9   # 10列目
        class_col = 12       # 13列目
        subclass_col = 13    # 14列目

        # ファイルに必要な列があるか確認
        required_cols = max(repeatname_col, class_col, subclass_col)
        if required_cols >= len(bed_df.columns):
            print(f"Error: The BED file does not contain the necessary columns (repeatname: 10, class: 13, subclass: 14).")
            sys.exit(1)

        # `repeatname` 列を取得し、NaNを除外
        bed_df = bed_df.dropna(subset=[repeatname_col])

        # `repeatname` ごとの出現回数をカウント
        repeatname_counts = bed_df[repeatname_col].value_counts().reset_index()
        repeatname_counts.columns = ["repeatname", "Number of lines"]

        # `repeatname` ごとの `class` および `subclass` を取得（最初にヒットした行）
        class_info = bed_df.groupby(repeatname_col).first()[[class_col, subclass_col]].reset_index()
        class_info.columns = ["repeatname", "class", "subclass"]

        # 出現回数データと結合
        result_df = pd.merge(repeatname_counts, class_info, on="repeatname", how="left")

        # 結果を表示
        print(result_df.to_string(index=False))

        # CSVに保存（指定があれば）
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