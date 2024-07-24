import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# 讀取CSV文件
data = pd.read_csv("C:/Users/KK Chan/Downloads/olist_order_reviews_dataset_translated01072024.csv")

# 獲取評論消息列的數據
review_messages = data['translated_comment']

# 創建一個空的詞語列表
words = []

# 遍歷每個評論消息
for message in review_messages:
    # 利用NLTK庫的詞語分詞功能將評論消息分詞並轉換為小寫
    tokens = word_tokenize(str(message).lower())
    # 過濾停用詞
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    # 將分詞結果添加到詞語列表中
    words.extend(tokens)

# 使用Counter進行詞語統計，獲取最常見的50個詞語
most_common_words = Counter(words).most_common(50)


# 輸出結果
for word, count in most_common_words:
    print(f'{word}: {count}')
print(most_common_words)
print(type(most_common_words))
