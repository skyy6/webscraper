#FJ-240213

from bs4 import BeautifulSoup
import os
import os.path
import pathlib
import html
import re


footer_text = ["0771-567 567","Viktiga datum för ditt företag","Här kan du få fram viktiga datum för ditt företag. Då kan du lätt se när du behöver betala in skatter, deklarera eller när du får utbetalningar.", "Läs mer om cookies", "På av.se använder vi cookies för att webbplatsen ska fungera på ett bra sätt för dig. Genom att surfa vidare godkänner du att vi använder cookies."
               , "ArbetsmiljöverketBox 9082 171 09 SolnaTelefon: 010-730 90 00", "Kontakta oss", "Kontakt", "Telefon:", "E-post:" ]

def sanitize_filename(filename):
    safe_filename = re.sub(r'[<>:"/\\|?*–”“]', '_', filename)
    safe_filename = safe_filename.strip()
    return safe_filename

def valid_check(tag):
    if(tag.parent.name == "li" or tag.parent.name == "td" or tag.find_parents("div", class_="updated rs_skip") or tag.find_parents("div", class_="imy-icon-link")):
        return False
    else:
        return True
    

       
def create_directory(orgname):
    os.makedirs(orgname, exist_ok=True)

def list_html_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if(file.endswith(".html")):
                file_list.append(os.path.join(root, file))
    return file_list

inputcase = input("Hitta <p> tag:")

if(inputcase.lower() == "ja"):
    sv = True
else:
    sv = False
    
rootpath = input("Rootpath:")
orgname = input("Myndighetsnamn:")
create_directory(orgname)
all_files = list_html_files(rootpath)


for file in all_files:
    with open(file, "r", encoding="utf-8") as html_code:
        soup = BeautifulSoup(html_code, "html.parser")
        
        title = soup.find("title").get_text()
            
        filename = orgname + "/" + sanitize_filename(title) + ".txt"
        with open(filename, "w", encoding="utf-8") as output:
        #output.write(title.get_text() + "\n")
            if(sv):
                
                html_list = soup.find_all("p")
                
                for tag in html_list:
                    if(tag.get_text() in footer_text):
                            html_list.remove(tag)
                            continue
                        
                    if(valid_check(tag)):
                        prev = tag.find_previous_sibling()
                        if prev and prev.name == "h2":
                            output.write(prev.get_text() + "\n" + tag.get_text() + "\n")
                        else:
                            output.write(tag.get_text() + "\n")
            else:
                main_container = soup.find(class_="main-content")
                if main_container:
                    output.write(main_container.get_text() + "\n")
                else:
                    print("No main found")
                            