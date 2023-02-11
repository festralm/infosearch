from index import Indexer

indexer = Indexer("test.txt")
indexer.add("1", "http://1", mode="w")  # overwrite if file exists
indexer.add("2", "http://2", mode="a")  # no overwrite if file exists
indexer.add("3", "http://3")  # no overwrite if file exists
indexer = Indexer("test.txt", overwrite=True)  # creates empty file
