import merge_csv as merge
import plot_results as plot

if __name__ == "__main__":
    df = merge.merge(save=False)
    plot.plot(df, show=False,save=True)
