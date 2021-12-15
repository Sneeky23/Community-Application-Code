from cassandra.cluster import Cluster
import matplotlib.pyplot as plt

tag_counter = {}

cluster = Cluster()
session = cluster.connect('community_app')

rows = session.execute('SELECT * FROM tag_like_count')

for user_row in rows:
    print(user_row)

    if user_row.tags in tag_counter.keys():
        tag_counter[user_row.tags] += user_row.count

    else:
        tag_counter[user_row.tags] = user_row.count

print(tag_counter)

plt.bar(range(len(tag_counter)), list(tag_counter.values()), align='center')
plt.xticks(range(len(tag_counter)), list(tag_counter.keys()))
plt.show()
