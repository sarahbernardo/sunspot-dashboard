
def get_mod(cycle_tuner):
    # calculate modulo of all decimal dates
    mod_df = df[start_yr:end_yr].copy()
    mod_df["Mod Res"] = mod_df["Date Fraction"] % cycle_tuner