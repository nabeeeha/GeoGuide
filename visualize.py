import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df_openai = pd.read_csv('embedding_openai1.csv')
df_gemini = pd.read_csv('embedding_gemini1.csv')


plt.figure(figsize=(10, 5))
plt.scatter(df_openai['No. of Characters'], df_openai['Time(s)'], label='OpenAI', alpha=0.5)
plt.scatter(df_gemini['No. of Characters'], df_gemini['Time(s)'], label='Gemini', alpha=0.5)
plt.title('Time Taken vs. Number of Characters')
plt.xlabel('Number of Characters')
plt.ylabel('Time (seconds)')
plt.legend()
plt.show()