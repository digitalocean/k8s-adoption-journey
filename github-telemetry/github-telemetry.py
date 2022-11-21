from github import Github
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

repository = "digitalocean/k8s-adoption-journey"
token = os.getenv('GITHUB_TOKEN')
views_headers = ["TotalDayViewCount", "UniqueViews", "Timestamp"]
clones_headers = ["Clones", "UniqueClones", "Timestamp"]

g = Github(token)

repo = g.get_repo(repository)

views = repo.get_views_traffic(per="day")
clones = repo.get_clones_traffic(per="day")

fileEmpty = os.stat("views.csv").st_size == 0

if __name__ == "__main__":

    with open('views.csv', 'a') as file_a:
        writer = csv.DictWriter(file_a, delimiter=',', fieldnames=views_headers)
        if fileEmpty:
            writer.writeheader()
        for view in views['views']:
            writer.writerow({'TotalDayViewCount': view.count, 'UniqueViews': view.uniques, 'Timestamp': view.timestamp.strftime("%m-%d-%Y")})

    with open('clones.csv', 'a') as file_b:
        writer = csv.DictWriter(file_b, delimiter=',', fieldnames=clones_headers)
        if fileEmpty:
            writer.writeheader()
        for clone in clones['clones']:
            writer.writerow({'Clones': clone.count, 'UniqueClones': clone.uniques, 'Timestamp': clone.timestamp.strftime("%m-%d-%Y")})
        

    def remove_duplicate_views(csv, duplicate_column):
        remove_duplicates_views = pd.read_csv(csv)
        no_duplicates_views = remove_duplicates_views.drop_duplicates(subset=[duplicate_column],keep='first')
        no_duplicates_views.to_csv(csv, index=False)
        return csv


    def create_data_frame(csv):
        data_frame = pd.read_csv(csv)
        return data_frame

    df_views = pd.DataFrame(create_data_frame('views.csv'))
    df_views.plot(x="Timestamp", y="TotalDayViewCount", kind='bar')
    plt.savefig('plot-views.png', dpi=300, bbox_inches='tight')

    df_clones = pd.DataFrame(create_data_frame('clones.csv'))
    df_clones.plot(x="Timestamp", y="Clones", kind='bar')
    plt.savefig('plot-clones.png', dpi=300, bbox_inches='tight')

    remove_duplicate_views('views.csv', 'Timestamp')
    remove_duplicate_views('clones.csv', 'Timestamp')

    



