from app.get_data import SQL

df_shareholders_change = SQL().get_diff_shares_primary()