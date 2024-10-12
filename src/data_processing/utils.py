import pandas as pd


def calculate_empty_goal_net(df: pd.DataFrame) -> pd.Series:
    """Determine if the goal net is empty"""
    return df.apply(lambda x: x['situationCode'][3] if x['teamSide'] == 'away' else x['situationCode'][0], axis=1).map(
        {'0': True, '1': False})


def determine_goal_advantage(df: pd.DataFrame) -> pd.Series:
    """Determine if the event team is in advantage, disadvantage, or neutral situation"""
    return df.apply(lambda x: "Advantage" if (int(x['situationCode'][1]) > int(x['situationCode'][2]) and x[
        'teamSide'] == 'away') or (int(x['situationCode'][2]) > int(x['situationCode'][1]) and x[
        'teamSide'] == 'home')
    else "Disadvantage" if (int(x['situationCode'][1]) < int(x['situationCode'][2]) and x['teamSide'] == 'away') or
                           (int(x['situationCode'][2]) < int(x['situationCode'][1]) and x['teamSide'] == 'home')
    else 'Neutral', axis=1)


def minutes_to_seconds(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Convert dataframe column from 'minutes:seconds' to 'seconds' and add the number of period
    """
    # Split columns into 'minutes' and 'seconds' and 'number of period' as integer
    df['minutes'] = df[column].str.split(':').str[0].astype(int)
    df['seconds'] = df[column].str.split(':').str[1].astype(int)
    df['numberPeriod'] = df['currentPeriod'].str.split("/").str[0].astype(int)

    # Total in seconds
    df[column] = df['minutes'] * 60 + df['seconds'] + 20 * 60 * (df['numberPeriod'] - 1)

    # Drop columns
    df.drop(['minutes', 'seconds', 'numberPeriod'], axis=1, inplace=True)

    return df[column]