import omnicare_tools.bloodpressure as ob
df = ob.Blood_pressure('03_bp_df.csv')
df.showhead(15)
df.preprocess('test22')
df.lineplot(saveFile=True)
df.errorbar(saveFile=True)
