from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, df):
        pass


# --------- сортування авторів ---------
class NameAscStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Author', ascending=True)


class NameDescStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Author', ascending=False)


class CountAscStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Count', ascending=True)


class CountDescStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Count', ascending=False)


# --------- сортування книг ---------
class TitleAscStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Title', ascending=True)


class TitleDescStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Book-Title', ascending=False)


class YearAscStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Year-Of-Publication', ascending=True)


class YearDescStrategy(SortingStrategy):
    def sort(self, df):
        return df.sort_values(by='Year-Of-Publication', ascending=False)
