import numpy as np
from scipy.stats import shapiro, mannwhitneyu, chi2_contingency, spearmanr
import pandas as pd

def load_data():
    df = pd.read_csv('clean_cvd.csv')
     # Pre-setting categorical data types to str to avoid issues with sns
    df[['smoke', 'alco', 'active', 'cardio', 'cholesterol', 'gluc','ap_aha', 'lifestyle', 'healthy_ls']] = df[['smoke', 'alco', 'active', 'cardio', 'cholesterol', 'gluc','ap_aha', 'lifestyle', 'healthy_ls']].astype('str') 

    # Setting relevant data types
    df[['sex', 'smoke', 'alco', 'active', 'cardio', 'lifestyle', 'healthy_ls']] = df[['sex', 'smoke', 'alco', 'active', 'cardio', 'lifestyle', 'healthy_ls']].astype('category')
    cat_gluc_chol = pd.CategoricalDtype(categories = ["1", "2", "3"], ordered = True)
    df[['cholesterol', 'gluc']] = df[['cholesterol', 'gluc']].astype(cat_gluc_chol)
    cat_aha = pd.CategoricalDtype(categories = ["1", "2", "3", "4"], ordered = True)
    df['ap_aha'] = df['ap_aha'].astype(cat_aha)
    cat_lifestyle = pd.CategoricalDtype(categories = ["0", "1", "2", "3", "4", "5", "6", "7"], ordered = False)
    df['lifestyle'] = df['lifestyle'].astype(cat_lifestyle)
    return df

def load_raw_data():
    return pd.read_csv('cardio_train.csv', sep = ";")

def pval_shapiro(df, var):
    pval = shapiro(df[var.name])[1]
    return f"Normally distributed <br>{pval_txt(pval)}" if pval >= 0.05 else f"Not normally distributed <br>{pval_txt(pval)}"

def pval_txt(pval):
    """
    Formats a p-value according to its value.

    If the p-value is less than 0.0001, the function returns the string 'p < 10^-4'.
    Otherwise, it returns the p-value rounded to 4 decimal places as a string, prefixed with 'p = '.

    Args:
        pval (float): The p-value to format.

    Returns:
        str: The formatted p-value.
    """
    if pval < 0.0001:
        return "<i>p</i> < 10⁻⁴"
    else:
        return f"<i>p</i> = {pval:.4f}"

def mean_sd_range(df, var):
    return (f"{np.mean(df[var.name]):.1f} ± {np.std(df[var.name]):.1f}", f"[{np.min(df[var.name]):.1f} - {np.max(df[var.name]):.1f}]")

def chi2_cardio(df, var):
    """
    Calculates the chi-squared statistic and p-value for a categorical variable in relation to 'cardio'.

    Parameters:
    - var (str): The name of the categorical variable in the DataFrame 'df'.

    Returns:
    - str: A text description of the p-value result.
    """
    crosstab = pd.crosstab(df[var.name], df['cardio'])
    chi2, pval, _, _ = chi2_contingency(crosstab)
    return pval_txt(pval)

def chi2_var(df, var1, var2):
    """
    Calculates the chi-squared statistic and p-value for a contingency table of two categorical variables.

    Parameters:
    - var1 (str): The name of the first categorical variable in the DataFrame 'df'.
    - var2 (str): The name of the second categorical variable in the DataFrame 'df'.

    Returns:
    - str: A text description of the p-value result.
    """
    crosstab = pd.crosstab(df[var1.name], df[var2.name])
    chi2, pval, _, _ = chi2_contingency(crosstab)
    return pval_txt(pval)

def mwu_cardio(df, var):
    """
    Computes a Mann-Whitney test for the difference in the input characteristic between patients with and without cardiovascular disease.

    Args:
    var: str
    The name of the characteristic to compare between patients with and without cardiovascular disease.

    Returns:
    pval: float
    The p-value of the Mann-Whitney U test.
    """
    mwu, pval = mannwhitneyu(df[df['cardio'] == "0"][var.name], df[df['cardio'] == "1"][var.name])
    return pval

def mean_sd(df, var):
    """
    Calculates the mean and standard deviation for a numerical variable in the DataFrame 'df' 
    and return the results as a formatted string.

    Parameters:
    - var (str): The name of the numerical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the mean and standard deviation in the format 'mean ± sd'.
    """
    return f'{np.mean(df[var.name]):.1f} ± {np.std(df[var.name]):.1f}'

def mean_sd_1(df, var):
    """
    Calculates the mean and standard deviation for a numerical variable in the subset of the DataFrame 'df' 
    where 'cardio' equals 1 and return the results as a formatted string.

    Parameters:
    - var (str): The name of the numerical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the mean and standard deviation in the format 'mean ± sd'.
    """
    return f'{np.mean(df[df.cardio == "1"][var.name]):.1f} ± {np.std(df[df.cardio == "1"][var.name]):.1f}'

def mean_sd_0(df, var):
    """
    Calculates the mean and standard deviation for a numerical variable in the subset of the DataFrame 'df' 
    where 'cardio' equals 0 and return the results as a formatted string.

    Parameters:
    - var (str): The name of the numerical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the mean and standard deviation in the format 'mean ± sd'.
    """
    return f'{np.mean(df[df.cardio == "0"][var.name]):.1f} ± {np.std(df[df.cardio == "0"][var.name]):.1f}'

def pp(df, var):
    """
    Calculates the percentage of positive occurrences (1) for a binary categorical variable in the DataFrame 'df' 
    and return the result as a formatted string.

    Parameters:
    - var (str): The name of the binary categorical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the percentage of positive occurrences in the format 'xx.x%'.
    """
    return f'{df[var.name].value_counts(normalize = True)[1]:.1%}'
    
def pp_0(df, var):
    """
    Calculates the percentage of positive occurrences (1) for a binary categorical variable in the subset of 
    the DataFrame 'df' where 'cardio' equals 0, and return the result as a formatted string.

    Parameters:
    - var (str): The name of the binary categorical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the percentage of positive occurrences in the format 'xx.x%'.
    """
    return f'{df[df.cardio == "0"][var.name].value_counts(normalize = True)[1]:.1%}'
    
def pp_1(df, var):
    """
    Calculates the percentage of positive occurrences (1) for a binary categorical variable in the subset of 
    the DataFrame 'df' where 'cardio' equals 1, and return the result as a formatted string.

    Parameters:
    - var (str): The name of the binary categorical variable in the DataFrame 'df'.

    Returns:
    - str: A formatted string representing the percentage of positive occurrences in the format 'xx.x%'.
    """
    return f'{df[df.cardio == "1"][var.name].value_counts(normalize = True)[1]:.1%}'

def pp_3_cardio(df, var, card):
    if card == "0":
        df = df[df['cardio'] == "0"]
    else:
        df = df[df['cardio'] == "1"]
    return f"""N: {df[var.name].value_counts(normalize = True)["1"]:.1%}
    <br>+: {df[var.name].value_counts(normalize = True)["2"]:.1%}
    <br>++: {df[var.name].value_counts(normalize = True)["3"]:.1%}
    """

def pp_3(df, var):
    return f"""N: {df[var.name].value_counts(normalize = True)["1"]:.1%}
    <br>+: {df[var.name].value_counts(normalize = True)["2"]:.1%}
    <br>++: {df[var.name].value_counts(normalize = True)["3"]:.1%}
    """

def pp_4_cardio(df, var, card):
    if card == "0":
        df = df[df['cardio'] == "0"]
    else:
        df = df[df['cardio'] == "1"]
    return f"""Normal: {df[var.name].value_counts(normalize = True)["1"]:.1%}
    <br>Elevated: {df[var.name].value_counts(normalize = True)["2"]:.1%}
    <br>High Blood Pressure stage I: {df[var.name].value_counts(normalize = True)["3"]:.1%}
    <br>High Blood Pressure stage II: {df[var.name].value_counts(normalize = True)["4"]:.1%}
    """

def pp_4(df, var):
    return f"""Normal: {df[var.name].value_counts(normalize = True)["1"]:.1%}
    <br>Elevated: {df[var.name].value_counts(normalize = True)["2"]:.1%}
    <br>High Blood Pressure stage I: {df[var.name].value_counts(normalize = True)["3"]:.1%}
    <br>High Blood Pressure stage II: {df[var.name].value_counts(normalize = True)["4"]:.1%}
    """