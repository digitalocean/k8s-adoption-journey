from github import Github
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

REPOSITORY = "digitalocean/k8s-adoption-journey"
GITHUB_TOKEN = "GITHUB_TOKEN"

if GITHUB_TOKEN not in os.environ:
        raise EnvironmentError(f"Failed because {GITHUB_TOKEN} is not set.")

token = os.getenv("GITHUB_TOKEN")
views_headers = ["TotalDayViewCount", "UniqueViews", "Timestamp"]
clones_headers = ["Clones", "UniqueClones", "Timestamp"]

def write_to_csv(csv_name, csv_headers, telemetry_data, data_dict, first_colum_name, second_column_name):
    """Creates separate CSVs with Github views and counts information"""
    fileExists = os.path.isfile(csv_name)
    with open(csv_name, 'a') as file:
        writer = csv.DictWriter(file, delimiter=',', fieldnames=csv_headers)
        if not fileExists:
            writer.writeheader()
        for data in telemetry_data[data_dict]:
            writer.writerow({first_colum_name: data.count, second_column_name: data.uniques, 'Timestamp': data.timestamp.strftime("%m-%d-%Y")})


def remove_duplicate_views(csv, duplicate_column):
    """Removes duplicate data based on the timestamp column"""
    remove_duplicates_views = pd.read_csv(csv)
    no_duplicates_views = remove_duplicates_views.drop_duplicates(subset=[duplicate_column],keep='first')
    no_duplicates_views.to_csv(csv, index=False)
    return csv

def create_data_frame(csv):
    """Creates the data frame which will be used to create images"""
    data_frame = pd.read_csv(csv)
    return data_frame

if __name__ == "__main__":  
    g = Github(token)
    repo = g.get_repo(REPOSITORY)
    views = repo.get_views_traffic(per="day")
    clones = repo.get_clones_traffic(per="day")
    
    write_to_csv('views.csv', views_headers, views, 'views' , 'TotalDayViewCount', 'UniqueViews')
    write_to_csv('clones.csv', clones_headers, clones, 'clones' , 'Clones', 'UniqueClones')

    remove_duplicate_views('views.csv', 'Timestamp')
    remove_duplicate_views('clones.csv', 'Timestamp')
        
    df_views = pd.DataFrame(create_data_frame('views.csv'))
    df_views.plot(x="Timestamp", y="TotalDayViewCount", kind='bar')
    plt.savefig('plot-views.png', dpi=300, bbox_inches='tight')

    df_clones = pd.DataFrame(create_data_frame('clones.csv'))
    df_clones.plot(x="Timestamp", y="Clones", kind='bar')
    plt.savefig('plot-clones.png', dpi=300, bbox_inches='tight')


    



