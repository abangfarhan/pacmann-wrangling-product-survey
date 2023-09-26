# Mini Project Wrangling Data Product Survey - Pacmann AI

## Instruction

Full instruction see [here](https://docs.google.com/document/d/1lJcWGQMDeKHxdl1EH1_rlWCI_NAcdhOAGmckBcB2ZVU/preview).

There are two data sources/input:

- `conjoint_survey_organic.xlsx - Sheet1.csv` ([source](https://docs.google.com/spreadsheets/d/1mDC2RlqFXh6zqtXgjfBZF_WHQ8ECpmb6/edit#gid=1453868824))
- `conjoint_survey_ads.csv` ([source](https://drive.google.com/file/d/1Hf6YCjnRI0YIk0H-IGQKgr3cmBKmVKzO/view))

The data are generated from [this survey](https://docs.google.com/forms/d/e/1FAIpQLScovDB2pyDd2iefKkQ4_ZB2keYkYaRNsIDRD39KKZee51OS1A/viewform). See that survey to find out each question's list of program details.

Need to:

- Filter invalid data: those that answers both "D" ("none of the above") and A-C at the same time.
- Clean and transform data into the following format:

| user_phone   | choice | skill                          | bentuk_program  | harga_program |
| ------------ | ------ | ------------------------------ | --------------- | ------------- |
| 05xx61268xxx | 0      | Design AB Test Experimentation | Tutorial Based  | Rp 300.000,0  |
| 05xx61268xxx | 1      | Perform Customer Segmentation  | Mentoring Based | Rp 350.000,0  |
| 05xx61268xxx | 0      | Design Data Pipeline           | Mentoring Based | Rp 550.000,0  |
| 08xx0007xxx  | 0      | Perform Churn Analytics        | Mentoring Based | Rp 450.000,0  |
| 08xx0007xxx  | 0      | Design AB Test Experimentation | Mentoring Based | Rp 500.000,0  |
| ...          | ...    | ...                            | ...             | ...           |

In other words, each question is turned into 3 lines (since there's 3 choice for each line), where the chosen option is set to "1" in column "choice".

Submit [here](https://docs.google.com/forms/d/e/1FAIpQLSdjKuj8xs7_yGzsfluNRGfcJ5A68CFz7LGqLJrMm1sq5kxFTg/viewform).

## Data Wrangling

The data wrangling is done in `clean_data.py` in this repo.
