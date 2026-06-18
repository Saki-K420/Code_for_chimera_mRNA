#%%
import sys, re

#%%
argvs = sys.argv
infile = str(argvs) ## input GTF file
outfile = str(argvs[2]) ## output of TSS bed file

with open(infile, 'r') as fr, open(outfile, 'w') as fw:
    for line in fr:  #１行づつ読む
        line = line.strip() # 行を文字列としてlineに代入する
        
        if line.startswith('#'):  # GFFファイルで"#"から始まる注釈はスキップ
            continue
            
        else:
            match = re.search(r'transcript_id\s+"([^"]+)"', line)  # line内にtranscript_id "XXXXX"というパターンがあるか
            if match:  # transcript_id "XXXXX"というパターンがあったら
                transcript_id = match.group(1)  # transcript_id "XXXXX"のXXXXXXの部分をtranscript_idに代入する
                
                columns = line.split('\t')  # 行をタブで区切ってリスト化してcolumnsに代入
                
                if columns[2] == 'transcript':  # もしcolumnsの2番め(リストは0始まり)が"transcript"だったら
                
                    if columns[6] == '+':  # プラス鎖の場合は転写物の5'端（columns[3]）の値で計算
                        # bed座標の形に整えて行に出力
                        fw.write(f'{columns[0]}\t{int(columns[3])-1}\t{int(columns[3])}\t{transcript_id}\t0\t{columns[6]}\n')
                        
                    elif columns[6] == '-':  # マイナス鎖の場合は転写物の3'端(columns[4])の値で計算
                        # bed座標の形に整えて行に出力
                        fw.write(f'{columns[0]}\t{int(columns[4])-1}\t{int(columns[4])}\t{transcript_id}\t0\t{columns[6]}\n')
# %%
