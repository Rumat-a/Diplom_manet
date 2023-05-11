import pandas as pd

data = {'name': ['Alice', 'Bob', 'Charlie', 'Dave'],
        'age': [25, 32, 18, 47],
        'city': ['London', 'Paris', 'New York', 'Sydney']}
print(data)
df = pd.DataFrame(data)
print(df.head(5))
