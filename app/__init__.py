import pandas as pd

from app.get_data import SQL

# df_shareholders_change = SQL().get_diff_shares_primary_with_feature()
# df_shareholders_change.to_csv("shareholders_changes_features.csv", index=False)


# temporary
from app.configs import ROOT_DIR
import os
import pandas as pd
df_shareholders_change = pd.read_csv(os.path.join(ROOT_DIR, "ext_data\shareholders_changes_features.csv"), index_col=False)