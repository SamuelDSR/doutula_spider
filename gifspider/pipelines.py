# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class GifspiderPipeline(object):
    """this pipeline amis to rite all crawled gifs or images into a organized csv,
    the content of the crawed gifs or images are downloaded using scrapy integrated
    image pipeline
    csv header:
        image_title, image_url, image_file, category (if only)
    """
    csv_fields = ["image_title", "image_url", "image_file"]

    def open_spider(self, spider):
        self.images_index_file = open("/home/shihe/gifspider/crawled_index.csv", "w", newline="")
        self.writer = csv.DictWriter(self.images_index_file, fieldnames=GifspiderPipeline.csv_fields)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.images_index_file.close()

    def process_item(self, item, spider):
        if len(item["images"]) == 0:
            raise DropItem("Failed to download image")
        
        index = {}
        index["image_title"] = item["image_title"]
        download_image_info  = item["images"][0]
        index["image_file"]  = download_image_info["path"]
        index["image_url"]   = download_image_info["url"]

        self.writer.writerow(index)
        return item
