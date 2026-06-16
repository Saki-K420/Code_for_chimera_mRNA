import pandas as pd
import sys
import csv

def extract_transcript_id(attribute_str):
    """GTFの属性列からtranscript_idを抽出"""
    return next((attr.split(' ')[1].replace('"', '') for attr in attribute_str.split(';') if attr.strip().startswith("transcript_id")), None)

def filter_gtf_by_bed(bed_file, gtf_file, output_file):
    try:
        # BEDファイルを読み込み（タブ区切り）
        bed_df = pd.read_csv(bed_file, sep='\t', header=None, usecols=[3, 5, 9, 11, 12, 13],
                             names=['bed_col4', 'tStrand', 'repeatname', 'rStrand', 'class', 'subclass'])
    except FileNotFoundError:
        print(f"Error: BED file '{bed_file}' not found.")
        sys.exit(1)

    try:
        # GTFファイルを読み込み（タブ区切り）
        gtf_df = pd.read_csv(gtf_file, sep='\t', header=None, comment='#', names=range(9))
    except FileNotFoundError:
        print(f"Error: GTF file '{gtf_file}' not found.")
        sys.exit(1)
    
    # 9列目のtranscript_idを抽出
    gtf_df['transcript_id'] = gtf_df[8].apply(extract_transcript_id)
    
    # 4列目の値とtranscript_idが一致する行を抽出
    filtered_gtf = gtf_df[gtf_df['transcript_id'].isin(bed_df['bed_col4'])]
    
    # BEDファイルの情報をtranscript_idをキーにしてグループ化し、ユニークな値を結合
    grouped = bed_df.groupby('bed_col4').agg(lambda x: ','.join(sorted(set(x.dropna())))).reset_index()
    
    # GTFとマージ
    annotated_gtf = filtered_gtf.merge(grouped, left_on='transcript_id', right_on='bed_col4', how='left')
    
    # 欠損値（NaN）を空文字列に変換
    annotated_gtf.fillna('', inplace=True)
    
    def format_attributes(row):
        """GTFの属性列をフォーマットし、新しい属性を追加"""
        attr = row[8].rstrip(';')  # 末尾のセミコロンを削除
        if row[2] == 'transcript':  # transcript行のみ修正
            attr += f'; class "{row["class"]}"; subclass "{row["subclass"]}"; repeatname "{row["repeatname"]}"'
            attr += f'; sense "{ "yes" if row["tStrand"] == row["rStrand"] else "no" }"'
        return attr
    
    # 新しい属性情報を追加
    annotated_gtf[8] = annotated_gtf.apply(format_attributes, axis=1)
    
    # 不要な列を削除（マージ用のcolを削除）
    annotated_gtf.drop(columns=['transcript_id', 'bed_col4', 'tStrand', 'repeatname', 'rStrand', 'class', 'subclass'], inplace=True)
    
    # 結果をGTF形式で保存
    annotated_gtf.to_csv(output_file, sep='\t', index=False, header=False, quoting=csv.QUOTE_NONE)
    
    print(f"Filtered GTF file saved to {output_file}")

if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) != 4:
        print("Usage: python script.py <bed_file> <gtf_file> <output_file>")
        sys.exit(1)
    
    # 入力ファイルと出力ファイルの取得
    bed_file, gtf_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    filter_gtf_by_bed(bed_file, gtf_file, output_file)