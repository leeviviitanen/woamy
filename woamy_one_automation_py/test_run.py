import pandas as pd

path_cache=r"C:\Users\ali_a\Downloads\woamy_one_automation_py\mem_cache.txt"
      
# reading the csv file
df = pd.read_csv(path_cache, index_col=False)

################################# INPUT VALUE ################################

foamer_air_ = 1
feeding_pump_ = 0
conveyer_belt_ = 0

##############################################################################

# updating the column value/data
df.loc[0,'foamer_air'] = str(foamer_air_)
df.loc[0,'feeding_pump'] = str(feeding_pump_)
df.loc[0,'conveyer_belt'] = str(conveyer_belt_)

# writing into the file
df.to_csv(path_cache, index=False)
print('Value changed')