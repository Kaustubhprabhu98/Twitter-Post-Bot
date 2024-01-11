from make_post import make_reddit_post, make_twitter_post
from fetch_query import fetch_query_data
import pandas as pd


def post_metrics(query, weeks, subreddit):
    graph_data = fetch_query_data(query, weeks)

    df = pd.DataFrame.from_dict(graph_data)
    mean_scores = df.mean()

    content = f"Analyzed posts from {query}\n" + \
              "\n".join(f"{metric}_score: {mean_scores[f'{metric}_score'].round(2)}"
                        for metric in ["stance", "toxicity", "controversy"])

    make_twitter_post(content)
    print("Made a twitter post")

    title = f"Insights for query {query}"
    make_reddit_post(subreddit, title, content.replace("\n", "\n\n"))
    print("Made a reddit post")


if __name__ == "__main__":
    post_metrics("(@Eskom_SA)", 1, "test")
