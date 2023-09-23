def plot_heatmap():
    uniform_data = np.random.rand(10, 12)
    ax = sns.heatmap(uniform_data, linewidth=0.5,cmap='winter',annot=True)
    plt.show()
    return

def plot_heatmap_result():
    rootDir = '/home/mehdi/PycharmProjects/pythonProject/result-heatmap/'
    csv_files = os.listdir(rootDir)
    for f in csv_files:
        # read the csv file
        path = os.path.join(rootDir, f)
        data = pd.read_csv(path)
        fig, ax = plt.subplots(figsize=(11,9))
        sns.heatmap(data.corr(), cmap='winter')
        plt.show()
    return