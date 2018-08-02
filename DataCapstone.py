   # PERFORMING SOME BASIC FUNCTIONS || DATA VISUALIZATION ON REAL WORLD DATASET i.e. 911.csv (in this case)
'''
Data columns (total 9 columns):
lat          99492 non-null float64
lng          99492 non-null float64
desc         99492 non-null object
zip          86637 non-null float64
title        99492 non-null object
timeStamp    99492 non-null object
twp          99449 non-null object
addr         98973 non-null object
e            99492 non-null int64
dtypes: float64(3), int64(1), object(5)
memory usage: 6.8+ MB
'''

# All the imports here:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df= pd.read_csv('911.csv')
# print(df.head())


# Checking the info. of the DataFrame
print(df.info())

# Check the DataFrame head
print(df.head())

# What are some top 3 ZIPCODES(zip) for 911 calls ?
print(df['zip'].value_counts().head(3))

# What are the top 5 townships(twp) for 911 calls ?
print(df['twp'].value_counts().head())

# How many unique title codes there in TITLE column ?
print(len(df['title'].unique()))    # df.['title'].unique() returns the array having all the unique title-codes

'''
In the title column there are "Reasons/Departments" specified before the title codes.
These are EMS, Fire and Traffic. Use .apply() with a custom lambda expression to create
a new column called "Reason" that contains this String value

For Example: if the title column is EMS:BACK PAINS/INJURY, the Reason column value would
be :- EMS
'''
ReasonName =  lambda title: title.split(':')[0]
df['Reason'] = df['title'].apply(ReasonName)

# What is the most common Reason for a 911 call based off this new column Reason ?
print(df['Reason'].value_counts())


# Create a seaborn COUNTPLOT of 911 calls by Reason
sns.countplot(x='Reason',data=df)
plt.show()


# Lets focus on the time information. What is the DataType of the objects in the timestamp column ?
print(type(df['timeStamp'].iloc[0]))

# These timeStamps are still the string. Lets convert them into DateTime Objects
df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# Now timeStamp column are actually DateTime objects.Create 3 Hours,Month and DayOfWeek new columns based off the timeStamp column

toHours = lambda time: time.hour
toMonth = lambda time:time.month
toDayOfWeek = lambda time:time.dayofweek
df['Hours'] = df['timeStamp'].apply(toHours)
df['Month'] = df['timeStamp'].apply(toMonth)
df['DayOfWeek'] = df['timeStamp'].apply(toDayOfWeek)

# Days of Week is an INTEGER. Use .map() to map the DayName according to the respective DayNumber
dict= {0:'Mon', 1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['DayOfWeek'] = df['DayOfWeek'].map(dict)


# Use the seaborn to cerate a COUNTPLOT of the DayOfWeek column with the hue based off the Reason column.
sns.countplot(x='DayOfWeek',data = df, hue = 'Reason')
plt.legend(bbox_to_anchor=(1.05,1),loc = 2, borderaxespad = 0.)
plt.show()



# if we plot the above graph but with Month column
sns.countplot(x='Month',data = df, hue = 'Reason')
plt.legend(bbox_to_anchor=(1.05,1),loc = 2, borderaxespad = 0.)
plt.show()


# we can see that some month's data is missing, lets try it with Linegraph and try some other visualization
byMonth = df.groupby('Month').count()
print(byMonth)

# Now show the simple plot indicating the number of calls made per month
byMonth['lat'].plot() # we assumes that if we have the latitude of the call, call actually took place
plt.show()



# Use lmplot() to create a linear fit on number of calls made per month
sns.lmplot(x='Month',y='lat',data=byMonth.reset_index())    #earlier Month was the index not the column so we need reset it
plt.show()


# Create a new column called 'Date' that contains the date from timeStamp column.
df['Date'] = df['timeStamp'].apply(lambda d: d.date())
print(df.head())


# Now groupby this Date Column and show how many calls are made per these Dates
test = df.groupby('Date').count()['lat']

test.plot()
plt.tight_layout()
plt.show()


# Recreate the above plot but 3 different plots, each representing Reason of the call
df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.show()
# same for the other Reasons i.e. Fire, EMS


