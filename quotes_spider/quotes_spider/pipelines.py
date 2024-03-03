import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file_quotes = open('quotes.json', 'w')
        self.file_authors = open('authors.json', 'w')

    def close_spider(self, spider):
        self.file_quotes.close()
        self.file_authors.close()

    def process_item(self, item, spider):
        if 'text' in item and 'author' in item and 'tags' in item:
            line = json.dumps(dict(item)) + "\n"
            self.file_quotes.write(line)
        elif 'name' in item and 'birth_date' in item and 'bio' in item:
            line = json.dumps(dict(item)) + "\n"
            self.file_authors.write(line)
        return item
