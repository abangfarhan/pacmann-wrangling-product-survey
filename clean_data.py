import pandas as pd

def clean_question_column(col: pd.Series) -> pd.Series:
    col = col.str.replace('. Tidak memilih semua product', '', regex=False)
    col = col.str.replace(' ', '')
    col = col.str.split(',')
    return col

def load_questions():
    # parse programs_specifications.txt
    # TODO specify that file format briefly
    with open('programs_specifications.txt', 'r') as f:
        text = f.read()

    programs = []
    for block in text.strip().split('---'):
        lines = block.strip().split('\n')
        number = int(lines[0])
        program_skills = lines[1].split(',')
        program_types = lines[2].split(',')
        program_prices = lines[3].split(',')
        program = []
        for pskill,ptype,pprice in zip(program_skills, program_types, program_prices):
            price = f"Rp {pprice.replace('_', '.')},0"
            program.append({'no': number, 'skill': pskill, 'bentuk_program': ptype, 'harga_program': price})
        programs.append(program)
    return programs


if __name__ == '__main__':
    df_org = pd.read_csv('./conjoint_survey_organic.xlsx - Sheet1.csv')
    df_ads = pd.read_csv('./conjoint_survey_ads.csv')
    df = pd.concat([df_org, df_ads]).reset_index(drop=True).drop('Timestamp', axis=1)

    # Clean question columns
    qcol_start = 1
    question_cols = [int(col.split('.')[0]) for col in df.columns[qcol_start:]]
    df.columns = ['user_phone', *question_cols]
    df.iloc[:,qcol_start:] = df.iloc[:,qcol_start:].apply(clean_question_column)
    # remove rows that choose "D" (i.e. "none of the above") but also choose other option
    is_invalid = df.iloc[:,qcol_start:].apply(lambda col: col.apply(lambda lst: 'D' in lst and len(lst) > 1)).any(axis=1)
    df = df[~is_invalid]

    df2 = df.melt(id_vars='user_phone', var_name='Question', value_name='Choices')
    letters = ('A', 'B', 'C')
    for letter in letters:
        df2[letter] = df2['Choices'].apply(lambda choices: letter in choices)

    df3 = (df2.drop('Choices', axis=1)
           .melt(id_vars=['user_phone', 'Question'], var_name='Option', value_name='Chosen?')
           .sort_values(['user_phone', 'Question', 'Option'])
           .reset_index(drop=True))
    df3['choice'] = df3['Chosen?'].astype(int)

    # make sure output is correct
    n_users = len(df['user_phone'].unique())
    n_choices = len(letters)
    n_questions = len(question_cols)
    assert len(df3) == n_users * n_choices * n_questions

    questions = load_questions()
    questions_flat = [val for sublist in questions for val in sublist] # flatten list
    dfq = pd.DataFrame(questions_flat)
    dfq['Option'] = ['A', 'B', 'C'] * len(questions)
    dfq2 = pd.concat([dfq] * n_users).reset_index(drop=True) # "repeat" the table n_users times

    df4 = pd.concat([df3, dfq2], axis=1)
    output = df4[['user_phone', 'choice', 'skill', 'bentuk_program', 'harga_program']]
    output.to_csv('clean_data.csv', index=False)
