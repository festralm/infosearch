class Indexer:

    def __init__(self, output_file, overwrite=True):
        self.output = output_file
        if overwrite:
            f = open(self.output, "w")
            f.write("")
            f.close()

    def add(self, file, link, mode="a"):
        f = open(self.output, mode)
        f.write(file)
        f.write(": ")
        f.write(link)
        f.write("\n")
        f.close()
