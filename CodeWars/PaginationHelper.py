# TODO: complete this class

class PaginationHelper:

    # The constructor takes in an array of items and a integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        self.collection = collection
        self.items_per_page = items_per_page

    def item_count(self):
        # returns the number of items within the entire collection

        return len(self.collection)

    def page_count(self):
        # returns the number of pages

        if len(self.collection) % self.items_per_page == 0:
            return len(self.collection) // self.items_per_page

        return len(self.collection) // self.items_per_page + 1

    def page_item_count(self, page_index):
        # returns the number of items on the current page. page_index is zero based
        # this method should return -1 for page_index values that are out of range

        items = [self.collection[i: i + self.items_per_page] for i in range(0, len(self.collection), self.items_per_page)]

        if page_index < 0 or page_index > len(items) - 1:
            return -1

        return len(items[page_index])

    def page_index(self, item_index):
        # determines what page an item is on. Zero based indexes.
        # this method should return -1 for item_index values that are out of range

        items = [self.collection[i: i + self.items_per_page] for i in range(0, len(self.collection), self.items_per_page)]

        if item_index < 0 or item_index > len(self.collection) - 1:
            return -1

        for index, value in enumerate(items):
            if self.collection[item_index] in value:
                return index


helper = PaginationHelper(['a', 'b', 'c', 'd', 'e', 'f'], 4)
print(helper.page_count())  # should == 2
print(helper.item_count())  # should == 6
print(helper.page_item_count(0))  # should == 4
print(helper.page_item_count(1))  # last page - should == 2
print(helper.page_item_count(2))  # should == -1 since the page is invalid

# page_index takes an item index and returns the page that it belongs on
print(helper.page_index(5))  # should == 1 (zero based index)
print(helper.page_index(2))  # should == 0
print(helper.page_index(20))  # should == -1
print(helper.page_index(-10))  # should == -1 because negative indexes are invalid
