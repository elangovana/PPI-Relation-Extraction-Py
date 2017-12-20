import bioc


class BiocLoader:

    def __init__(self):
        pass

    def parse(self, filename):
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            print(bioc.dumps(collection, pretty_print=True))
