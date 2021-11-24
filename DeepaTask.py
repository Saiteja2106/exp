import subprocess
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

def run_pull_command():
    return subprocess.check_output(["git","pull"])

def read_csv():
    df = pd.read_csv("input/Cleanseddata.csv")
    return df

def run_add_command():
    return subprocess.check_output(["git","add","."])

def run_push_command():
    return subprocess.check_output(["git", "push"])


def run_commit_command():
    today = datetime.now().date()
    return subprocess.check_output(["git","commit","-m",f"Adding {today} Plots"])

def do_visulaize(df):
    df.dropna(inplace=True)
    df[df['Location'] == "windham"]['Location'] = "Windham"
    df['Graduation Year'] = pd.to_numeric(df['Graduation Year'])
    location = df.groupby(['Location','Current Position']).size().reset_index(name='counts')
    cp = df.groupby(['Current Position']).size().reset_index(name='counts')
    degree = df.groupby(["Degree",'Current Position','Location', 'Graduation Year','Major']).size().reset_index(name='counts')
    fig = px.bar(cp, x= 'Current Position', y = 'counts')
    fig1 = px.scatter_3d(location, x='Location', y='Current Position', z='counts',color='counts')
    fig2 = px.scatter_3d(degree, x='Major', y='Current Position', z='counts',color='counts')
    fig3 = px.sunburst(degree, path=['Degree','Location','Current Position'], values='counts')
    if not os.path.exists("output"):
        os.makedirs("output")
    with open('output/graphs.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))

if __name__ =="__main__":
    run_pull_command()
    print("PULLED Successfully")
    df = read_csv()
    print("CsV file read.")
    do_visulaize(df)
    print("PLotting done")
    run_add_command()
    run_commit_command()
    run_push_command()