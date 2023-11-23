import os #provides a way to interact with the underlying operating system, such as working with files and directories, manipulating paths
import pickle #allows you to serialize and deserialize Python objects into a byte stream. Serialization is the process of converting an object into a format that can be stored or transmitted, while deserialization is the process of converting the serialized byte stream back into the original object.
import PySimpleGUI as sg # downloaded by pip install PySimpleGUI and used to create an interface
from typing import Dict

sg.ChangeLookAndFeel('Black')


class Gui:
    ''' Create a GUI object '''
    #constructor method init (par defaut) 
    def __init__(self):
        self.layout: list = [
            [sg.Text('Search Term', size=(11, 1)), #creates a new text element with the label "search term"
             sg.Input(size=(40, 1), focus=True, key="TERM"),   #creates a new input element
             sg.Radio('Contains', size=(10, 1), group_id='choice', key="CONTAINS", default=True),
             sg.Radio('StartsWith', size=(10, 1), group_id='choice', key="STARTSWITH"),
             sg.Radio('EndsWith', size=(10, 1), group_id='choice', key="ENDSWITH")],
            [sg.Text('Root Path', size=(11, 1)),
             sg.Input('/..', size=(40, 1), key="PATH"),
             sg.FolderBrowse('Browse', size=(10, 1)),
             sg.Button('Re-Index', size=(10, 1), key="INDEX"),
             sg.Button('Search', size=(10, 1), bind_return_key=True, key="SEARCH")],
            [sg.Output(size=(100, 30))]]

        self.window: object = sg.Window('File Search Engine', self.layout, element_justification='left')


class SearchEngine:
    ''' Create a search engine object '''

    def __init__(self):
        self.file_index = []  # directory listing returned by os.walk()
        self.results = []  # search results returned from search method
        self.matches = 0  # count of records matched
        self.records = 0  # count of records searched

    def create_new_index(self, values: Dict[str, str]) -> None:
        ''' Create a new file index of the root; then save to self.file_index and to pickle file '''
        root_path = values['Path']
        #create a new index
        self.file_index: list = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save index to file as a pickle file
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self) -> None:
        ''' Load an existing file index into the program '''
        #we use try except because if there is no pickle file the index_file list will be empty
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values: Dict[str, str]) -> None:
        ''' Search for the term based on the type in the index; the types of search
            include: contains, startswith, endswith; save the results to file '''
        #reset variables: counters are returned to 0 and the result list is clear
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['TERM']

        # search for matches and count results
        #find the term we're searching for in file_index(each row in the file index is a path)
        for path, files in self.file_index:
            for file in files:  #2 for loops one for the path and the second for each file inside the path
                self.records += 1  #for each file we find w increment records counter with +1
                #test 3 search options to know which one has the search term using if or loop
                if (values['CONTAINS'] and term.lower() in file.lower() or
                        values['STARTSWITH'] and file.lower().startswith(term.lower()) or  
                        values['ENDSWITH'] and file.lower().endswith(term.lower())):           #we use .lower because python is sensible a la case

                    result = path.replace('\\', '/') + '/' + file  #creating a full file path
                    self.results.append(result)
                    self.matches += 1  #increment the matches to keep count
                else:
                    continue

                    # save results to file
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    ''' The main loop for the program '''
    g = Gui()
    s = SearchEngine()
    s.load_existing_index()  # load if exists, otherwise return empty list

    while True:
        event, values = g.window.read()

        if event is None:
            break
        if event == 'INDEX':
            s.create_new_index(values)
            print()
            print(">> New index created")
            print()
        if event == 'SEARCH':
            s.search(values)

            # print the results to output element
            print()
            for result in s.results:
                print(result)

            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(s.records, s.matches))
            print(">> Results saved in working directory as search_results.txt.")


if __name__== '_main_':
    print('Starting program...')
    main()
    

