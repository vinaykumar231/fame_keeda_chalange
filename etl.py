import csv
import random

# Define how many rows you want
num_rows = 10000
filename = 'performance.csv'

# Write the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['campaignId', 'influencerId', 'likes', 'comments', 'shares', 'views'])

    for i in range(num_rows):
        campaign_id = random.randint(100, 110)  # 10 campaigns
        influencer_id = f'influencer_{random.randint(1, 1000)}'
        likes = random.randint(10, 5000)
        comments = random.randint(5, 1000)
        shares = random.randint(0, 500)
        views = random.randint(likes + comments + shares + 1, 100000)  # ensure views > interactions
        writer.writerow([campaign_id, influencer_id, likes, comments, shares, views])

print(f'Dummy data written to {filename}')
