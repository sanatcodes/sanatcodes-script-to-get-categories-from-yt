# YT API Video Aggregator 📹
This script accesses the YouTube API to fetch videos, aggregates their categories, and outputs the results as a CSV file.

## 🚀 Getting Started
To run the script, you'll need to install the required packages using pip:


```pip install -r requirements.txt```
You'll also need to obtain an API key from the YouTube Data API v3.

## 📝 Usage
To run the script, simply execute main.py:

python ```main.py```
By default, the script fetches the most popular videos from the YouTube API and aggregates them by category. You can also specify a specific country or category to fetch videos from by passing arguments:

```
python main.py --country US
python main.py --category Music
```
The results are output as a CSV file in the output folder.

🤖 Acknowledgements
This script is inspired by the work of [Syahrul Hamdani](https://syahrulhamdani.medium.com/) on the [Indonesia's Trending YouTube Video Statistics dataset](https://www.kaggle.com/datasets/syahrulhamdani/indonesias-trending-youtube-video-statistics).

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
