import os
import pandas as pd


def main():
    print(os.listdir('.'))
    psy_tar_dir = 'PsyTar/'
    pass
    adr_csv_path = os.path.join(psy_tar_dir, 'ADR_Identified.csv')
    di_csv_path = os.path.join(psy_tar_dir, 'DI_Identified.csv')
    ssi_csv_path = os.path.join(psy_tar_dir, 'SSI_Identified.csv')
    wd_csv_path = os.path.join(psy_tar_dir, 'WD_Identified.csv')
    sent_labeling_csv_path = os.path.join(psy_tar_dir, 'Sentence_Labeling.csv')

    adr_df = pd.read_csv(adr_csv_path, encoding="utf-8")
    di_df = pd.read_csv(di_csv_path, encoding="utf-8")
    ssi_df = pd.read_csv(ssi_csv_path, encoding="utf-8")
    wd_df = pd.read_csv(wd_csv_path, encoding="utf-8")
    sent_labeling_df = pd.read_csv(sent_labeling_csv_path, encoding="utf-8")

    resulting_df = sent_labeling_df[["drug_id", "sentence_index", "EF", "INF"]]
    print(resulting_df)

    adr_range = [f"ADR{i}" for i in range(1, 31)]
    adr_df["adr_count"] = adr_df.apply(lambda row: row[adr_range].notnull().sum(), axis=1)
    wd_range = [f"WD{i}" for i in range(1, 10)]
    wd_df["wd_count"] = wd_df.apply(lambda row: row[wd_range].notnull().sum(), axis=1)
    ssi_range = [f"SSI{i}" for i in range(1, 10)]
    ssi_df["ssi_count"] = ssi_df.apply(lambda row: row[ssi_range].notnull().sum(), axis=1)
    di_range = [f"DI{i}" for i in range(1, 10)]
    di_df["di_count"] = di_df.apply(lambda row: row[di_range].notnull().sum(), axis=1)
    # todo: Select only neeed columns, merge

    # todo: Для того, что сделать агрегацию, взять строки, у которых нужный каунт не нулевой
    # todo: А потом на отобранных строках посчитать суммы по соответствующим колонкам


if __name__ == '__main__':
    main()
