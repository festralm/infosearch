class Indexer:

    def __init__(self, output_file):
        self.output = output_file

    def add(self, file, link, mode="a"):
        f = open(self.output, mode)
        f.write(file)
        f.write(": ")
        f.write(link)
        f.write("\n")
        f.close()
