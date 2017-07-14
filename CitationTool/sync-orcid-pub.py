import requests
import json
import re
import bibtexparser

##### class for humanName #####
class humanName:
    # Necessary Variables
    firstName = None
    middleName = None
    lastName = None
    nameTextOutput = ""

    def __init__(self, nameString):
        if ',' in nameString:
            nameDecomposition = re.split(r"\s*,\s*",nameString)
            self.lastName = nameDecomposition[0]
            FirstMiddleName = nameDecomposition[1]
            FirstMiddleNameDecomposition = re.split(r"\s+",FirstMiddleName)
            if len(FirstMiddleNameDecomposition)<=1:
                self.firstName = FirstMiddleNameDecomposition[0]
            else:
                self.firstName = FirstMiddleNameDecomposition[0]
                ## should strip out '.'
                self.middleName = FirstMiddleNameDecomposition[1]
        else:
            nameDecomposition = re.split(r"\s+",nameString)
            self.firstName = nameDecomposition[0]
            if len(nameDecomposition)==2:
                self.lastName = nameDecomposition[1]
            elif len(nameDecomposition)==3:
                self.middleName = nameDecomposition[1]
                self.lastName = nameDecomposition[2]
            else:
                print(nameDecomposition)
                pass

    def __repr__(self):
        return "<human name object, first name: %s, middle name: %s, last name: %s>" \
            %(self.firstName, self.middleName, self.lastName)

    def outputText(self):
        if self.middleName:
            return self.firstName[0]+ ". "+ self.middleName[0]+ ". "+ self.lastName
        else:
            return self.firstName[0]+ ". "+ self.lastName


html_file = open("list-publications.html","w")

##### Retreive Data from Orcid #####
url = "http://orcid.org/0000-0002-1968-5092/orcid-works"
headers = {'Accept': 'application/orcid+json'}
response = requests.get(url, headers=headers)
jsonroot = response.json()
myactivities = jsonroot["orcid-profile"]["orcid-activities"]

##### Parse Publication Entry and Output #####
for workitem in myactivities["orcid-works"]["orcid-work"]:
    bib_text = workitem["work-citation"]["citation"]
    bib_database = bibtexparser.loads(bib_text)
    bib_entry = bib_database.entries[0]

    entry_html = ""

    ##### Parse Author List #####
    author_list = re.split(r"\s+and\s+",bib_entry["author"])
    # print('--------\n')
    # print(author_list)
    # print('--------\n')
    author_Num = len(author_list)

    if author_Num == 1:
        authorNameString = author_list[0]
        authorNameObj = humanName(authorNameString)
        author_text = authorNameObj.outputText()
    else:
        author_text = ""
        for authorID in range(0,author_Num):
            authorNameString = author_list[authorID]
            authorNameObj = humanName(authorNameString)
            author_text = author_text+ authorNameObj.outputText()
            if authorID < author_Num - 2:
                author_text = author_text+ ", "
            elif authorID < author_Num - 1:
                author_text = author_text+ " and "
            else:
                pass

    ##### Assemble Work Entry #####

    # Author List
    author_text = re.sub(r"Y\. Xue", "<b>Y. Xue</b>", author_text) # Highlight Myself
    entry_html = entry_html+ author_text+ ", "

    # Article Title
    entry_html = entry_html+ "\""+ bib_entry["title"]+ "\""+ ", "

    # Journal
    entry_html = entry_html+ "<i>"+ bib_entry["journal"]+ "</i>"+ " "

    # Volume, Pages, Year
    try:
        entry_html = entry_html+ bib_entry["volume"]+ ", "
    except:
        pass
    try:
        entry_html = entry_html+ bib_entry["pages"]+ " "
    except:
        pass
    entry_html = entry_html+ "("+ bib_entry["year"]+ ")"

    # Wrap and write entry to file
    entry_html = "<li>"+ entry_html + "</li>"+ "\n"
    html_file.write(entry_html)

html_file.close()
