

#Setting Crosswalk data
AI_Active_map = dict(Xwalk_DF.set_index('AI_Code').Xwalk_DF['AI_Code_Active (2018-19)'])
Internal_df['Active AI'] = Internal_df['AI Code'].map(AI_Active_map)

FSC_map = dict(Xwalk_DF.set_index('AI_Code').Xwalk_DF['B/CO'])
Internal_df['FSC'] = Internal_df['AI_Code'].map(FSC_map)

#Setting Coordinator data
SD_map = dict(Coordinator_DF.set_index('AI Code').Coordinator_DF['SD_Name'])
Internal_df['SAT Coordinator'] = Internal_df['AI_Code'].map(SD_map)

#Setting Ordering data
TOS_map = dict(Ordering_DF.set_index('AI Code').Coordinator_DF['TOS Access Code'])
Internal_df['TOS ACCESS'] = Internal_df['AI_Code'].map(TOS_map)

ShouldPSAT_map = dict(Ordering_DF.set_index('AI Code').Coordinator_DF['PSAT Should'])
Internal_df['PSAT Order'] = Internal_df['AI_Code'].map(ShouldPSAT_map)

#and so on...