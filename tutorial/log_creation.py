from scraping_rss import *
import requests,bs4,csv


def main():
    output_array = []
    for i, url in enumerate(url_list):
        rss_meta_list = scraping(url)
        output_array.append(rss_meta_list)

    print(output_array)
    output_csv(output_array)

if __name__ == '__main__':
    main()
