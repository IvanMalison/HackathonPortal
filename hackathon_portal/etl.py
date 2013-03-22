import csv

class Extractor(object):

    def extract(self, identifier):
        raise NotImplemented()


class Transformer(object):

    def transform(self, raw_data):
        raise NotImplemented()


class Loader(object):

    def load(self, transformed):
        raise NotImplemented()


class ETL(object):

    # `extractor` should be an object that knows how to fetch data to be
    # transformed from a single argument.
    extractor = None

    # `transformers` should be a dictionary of transformation objects that should be
    # applied to extracted data.
    transformers = None

    # `loader` should be a loader instance. It should operate on a dictionary of
    # transformed values

    def __init__(self, identifier):
        self.identifier = identifier
        self.raw_data = None
        self.transformed = {}

    def execute(self):
        self.extract()
        self.transform()
        return self.load()

    def extract(self):
        self.raw_data = self.extractor.extract(self.identifier)
        return self.raw_data

    def transform(self):
        self.transformed.update(
            {
                key: transformer.transform(self.raw_data)
                for key, transformer in self.transformers.iteritems()
            }
        )

    def load(self):
        return self.loader.load(self.transformed)


class CSVExtractor(Extractor):

    def extract(self, filename):
        with open(filename, 'rU') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            extracted_data = [row for row in csv_reader]

            return extracted_data