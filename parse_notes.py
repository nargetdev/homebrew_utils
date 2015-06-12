import codecs
import re
import vim
import markdown
import webbrowser

from os.path import expanduser
home = expanduser("~")

section_list = {}
hunk = []
section=False

buf = vim.current.buffer
cur_section=""
for word in buf:
    #regexp that matches the date tag
    if (re.match(".*[0-9]{2}:[0-9]{2}:[0-9]{2}.*",word) ):
        current_date = word
    if (re.match("---",word)):
        section=False
    if section:
        section_list[cur_section].append((word,current_date))
    if (re.match("\s*[A-Z\ ]+:",word)):
        section=True
        cur_section=word
        if cur_section not in section_list:
            section_list[cur_section] = []


last = ""
my_text_string = ""
for category in section_list:
    #print category
    my_text_string += "\n\n\n###" + category + '\n\n'
    for item in section_list[ category ]:
        if last != item[1]:
            #print item[1]
            my_text_string += "*" + item[1] + '\n\n'
            last = item[1]
        #print item[0]
        my_text_string += item[0] + '\n\n'


#print my_text_string
my_text_string = unicode(my_text_string, "utf-8")
html = markdown.markdown(my_text_string)
#print html

print home
output_file = codecs.open(home+"/some_file.html", "w",
                          encoding="utf-8",
                          errors="xmlcharrefreplace"
)
output_file.write(html)

webbrowser.open("file://"+home+"/some_file.html")
