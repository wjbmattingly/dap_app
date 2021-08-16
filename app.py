import streamlit as st
import glob
import json
import spacy_streamlit
import streamlit.components.v1 as components
import pandas as pd

spacy_model = "models/latin_ruler_backup"

visualizers = ["entity_ruler"]

# st.title("The Digital Alcuin Project")
st.image("header.png")

st.sidebar.image("logo.png")
st.sidebar.write("<b>Disclaimer</b>: This App is in Alpha Testing.<br>It is currently at version <b>0.0.4</b>.<br>Much of the data remains to be manually validated.", unsafe_allow_html=True)
st.sidebar.header("Choose App Task")

options = st.sidebar.selectbox("Select Mode",
                    ("Letter Mode", "NER Mode", "Side-by-Side Mode", "Alcuin's Epistolary Network", "Database Mode", "About Project", "Sources for Data"))

with open ("data/letter_page_spans.json", "r") as f:
    page_spans = json.load(f)

with open ("data/letter_header.json", "r") as f:
    headers = json.load(f)

with open ("data/letter_people.json", "r") as f:
    letter_people = json.load(f)

with open ("data/pase_keys.json", "r") as f:
    pase_keys = json.load(f)

with open ("data/scrip_refs_pages_clean.json", "r") as f:
    scrip_pages = json.load(f)

files = glob.glob("data/cleaned_letters/*txt")
letter_nums = []
for file in files:
    file = file.split("cleaned_letters_")[1].replace(".txt", "")
    ep = f"Ep. {file}"
    letter_nums.append(ep)
letter_nums.sort()

if options == "Side-by-Side Mode":
    add_selectbox = st.selectbox("Select Letter", letter_nums)
    col1, col2 = st.beta_columns(2)
    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()


    clean_ep = ep_file.lstrip("0")
    col1.header(f"Letter {clean_ep} Text")
    clean_ep = ep_file.lstrip("0")
    letter_header = headers[clean_ep]

    cod = letter_header["cod"]
    ed = letter_header["ed"]
    expand_data = col1.beta_expander("Manuscripts")
    expand_data.write(f"Manuscripts (unvalidated): {cod}")

    people = letter_people[clean_ep]
    people_keys = []
    all_keys = list(pase_keys.keys())
    all_people_html = []
    for person in people:
        if person != "":
            if person in all_keys:
                k = pase_keys[person]
                url = f"https://pase.ac.uk/jsp/DisplayPerson.jsp?personKey={k}"
                all_people_html.append(f'<a href="{url}" target="_blank">{person}</a>')
            else:
                all_people_html.append(person)
    all_html = ", ".join(all_people_html)

    expand_people = col1.beta_expander("People Referenced (PASE Data)")
    expand_people.markdown(f"People Referenced: {all_html}", unsafe_allow_html=True)


    desc = letter_header["description"]
    col1.write(f"Description: {desc}")
    col1.write(letter_header["salutation"])
    col1.write("\n")

    col1.write(letter)

    image_list = page_spans[clean_ep]
    all_images = []
    for i in range(image_list[0], image_list[1]+1):
        all_images.append(i)

    scrip_refs = []
    for image in all_images:
        new = int(image)
        i = int(new)
        if i < 10:
            new_i = f"00{i}"
        elif i < 100 and i > 9:
            new_i = f"0{i}"
        else:
            new_i = i

        refs = scrip_pages[new_i]
        for r in refs:
            if "MANUAL" not in r:
                if len(r) == 3:
                    book, chapter, verse = r
                    d = f"{book}. {chapter}, {verse}"
                    scrip_refs.append(d)
                elif len(r) == 2:
                    book, chapter = r
                    d = f"{book}. {chapter}"
                    scrip_refs.append(d)
    scrip_expander = st.sidebar.beta_expander(f"Scripture References ({len(scrip_refs)})")
    refs_html = "<br>".join(scrip_refs)
    scrip_expander.write(refs_html, unsafe_allow_html=True)

    col2.header(f"Letter {clean_ep} Image(s)")
    # col2.write(clean_ep)
    for image in all_images:
        new = int(image)-16
        i = int(new)
        if i < 10:
            new_i = f"00{i}"
        elif i < 100 and i > 9:
            new_i = f"0{i}"
        else:
            new_i = i
        image_name = f"data/adobe_images/letters-Copy1_Page_{new_i}_Image_0001.jpg"
        col2.image(image_name)


elif options == "Letter Mode":
    add_selectbox = st.selectbox("Select Letter", letter_nums)
    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()
    clean_ep = ep_file.lstrip("0")
    letter_header = headers[clean_ep]

    st.header(f"Letter {clean_ep} Text")
    cod = letter_header["cod"]
    ed = letter_header["ed"]


    expand_data = st.beta_expander("Manuscripts")
    expand_data.write(f"Manuscripts (unvalidated): {cod}")

    people = letter_people[clean_ep]
    people_keys = []
    all_keys = list(pase_keys.keys())
    all_people_html = []
    for person in people:
        if person != "":
            if person in all_keys:
                k = pase_keys[person]
                url = f"https://pase.ac.uk/jsp/DisplayPerson.jsp?personKey={k}"
                all_people_html.append(f'<a href="{url}" target="_blank">{person}</a>')
            else:
                all_people_html.append(person)
    all_html = ", ".join(all_people_html)

    expand_people = st.beta_expander("People Referenced (PASE Data)")
    expand_people.markdown(f"People Referenced: {all_html}", unsafe_allow_html=True)


    desc = letter_header["description"]
    st.write(f"Description: {desc}")
    # st.write(letter_header["description"])
    st.write(letter_header["salutation"])
    st.write("\n")
    st.write(letter)


elif options == "NER Mode":
    add_selectbox = st.selectbox("Select Letter", letter_nums)
    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()
    doc = spacy_streamlit.process_text(spacy_model, letter)

    spacy_streamlit.visualize_ner(
        doc,
        labels=["PERSON", "GROUP", "PLACE"],
        show_table=False
    )
    # st.sidebar.write(doc.ents)
    found_people = []
    found_groups = []
    found_places = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in found_people:
                found_people.append(ent.text)
        elif ent.label_ == "GROUP":
            if ent.text not in found_group:
                found_group.append(ent.text)
        elif ent.label_ == "PLACE":
            if ent.text not in found_place:
                found_place.append(ent.text)
    found_people.sort()
    found_groups.sort()
    found_places.sort()

    person_expander = st.sidebar.beta_expander(f"Found People ({len(found_people)})")
    person_html = "<br>".join(found_people)
    person_expander.write(person_html, unsafe_allow_html=True )

    group_expander = st.sidebar.beta_expander(f"Found Groups ({len(found_groups)})")
    group_html = "<br>".join(found_groups)
    group_expander.write(group_html, unsafe_allow_html=True )

    place_expander = st.sidebar.beta_expander(f"Found Places  ({len(found_places)})")
    place_html = "<br>".join(found_places)
    place_expander.write(place_html, unsafe_allow_html=True )


elif options == "Alcuin's Epistolary Network":
    with open ("data/alcuin_all_letters.html", 'r', encoding='utf-8') as f:
        source_code = f.read()
    components.html(source_code, height = 1200,width=1000)

elif options == "Database Mode":
    # df =  pd.read_csv("data/database.csv")
    pass

elif options == "About Project":
    st.write('This project was designed by <a href="https://wjbmattingly.com" target="_blank">William Mattingly</a> as part of a larger project, <a href="https://pythonhumanities.com" target="_blank">PythonHumanities.com</a> to provide the letters of Alcuin in raw text alongside their MGH editions with named entity-recognition and Scriptural and Patristic sources extracted from the text. It is currently in Alpha. The data needs to be manually validated still.<br><br>For each letter available, we have linked to letter to the <a href="https://pase.ac.uk/" target="_blank">PASE (Prosopography of Anglo-Saxon England)</a> dataset of Alcuin\'s letters which include all individuals cited in or recipients of the letters. Each individual has their unique PASE-ID and is hyper-linked to the PASE database.', unsafe_allow_html=True)

elif options == "Sources for Data":
    st.write("All Persons, Prosopography of Anglo-Saxon England, http://www.pase.ac.uk, accessed 15 August 2021.")






#
