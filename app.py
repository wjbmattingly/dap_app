import streamlit as st
import glob
import json
import spacy_streamlit
import streamlit.components.v1 as components
import pandas as pd
from ast import literal_eval

st.set_page_config(layout="wide")


# st.write(df)
spacy_model = "models/latin_ruler_backup"

visualizers = ["entity_ruler"]

# st.title("The Digital Alcuin Project")
st.image("header.png")

st.sidebar.image("logo.png")
st.sidebar.write("<b>Disclaimer</b>: This App is in Alpha Testing.<br>It is currently at version <b>0.0.4</b>.<br>Much of the data remains to be manually validated.", unsafe_allow_html=True)
st.sidebar.header("Choose App Task")

options = st.sidebar.selectbox("Select Mode",
                    ("Letter Mode", "NER Mode", "Side-by-Side Mode", "Alcuin's Epistolary Network", "Textual Network", "Database Mode", "About Project", "Sources for Data"))

if options == "Letter Mode" or options == "NER Mode" or options == "Side-by-Side Mode":
    with open ("data/scrip_refs_pages_clean.json", "r") as f:
        scrip_pages = json.load(f)


    files = glob.glob("data/cleaned_letters/*txt")
    letter_nums = []
    for file in files:
        file = file.split("cleaned_letters_")[1].replace(".txt", "")
        ep = f"Ep. {file}"
        letter_nums.append(ep)
    letter_nums.sort()
    add_selectbox = st.selectbox("Select Letter", letter_nums)

    df = pd.read_csv("data/dap_dataset.csv")

    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()

    letter_data = df.loc[df['letter_num'] == f"Ep. {ep_file}"]

    cleaned_mss = st.expander("Manuscripts")

    cleaned_mss.write(letter_data.iloc[0]["valid_mss"])


    expand_data = st.expander("Manuscripts OCR")
    expand_data.write(f"Manuscripts (unvalidated): "+ letter_data.iloc[0]["mss_ocr"])

    people = literal_eval(letter_data.iloc[0]["pase_refs"])
    keys = literal_eval(letter_data.iloc[0]["pase_keys"])


    all_people_html = []
    n = 0
    for person in people:
        k = keys[n]
        url = f"https://pase.ac.uk/jsp/DisplayPerson.jsp?personKey={k}"
        all_people_html.append(f'<a href="{url}" target="_blank">{person}</a>')
    all_html = ", ".join(all_people_html)

    expand_people = st.expander("People Referenced (PASE Data)")
    expand_people.markdown(f"People Referenced: {all_html}", unsafe_allow_html=True)
    if options == "Letter Mode" or options == "NER Mode":
        desc = letter_data.iloc[0]["description"]
        st.write(f"Description: {desc}")

        salutation = letter_data.iloc[0]["salutation"]
        salutation_html = f"<center>{salutation}</center>"
        st.write(salutation_html, unsafe_allow_html=True)
        st.write("\n")

if options == "Side-by-Side Mode":
    col1, col2 = st.beta_columns(2)
    col1.header(f"Letter {ep_file} Text")
    desc = letter_data.iloc[0]["description"]
    col1.write(f"Description: {desc}")

    salutation = letter_data.iloc[0]["salutation"]
    salutation_html = f"<center>{salutation}</center>"
    col1.write(salutation_html, unsafe_allow_html=True)
    col1.write("\n")

    letter = letter.split("\n\n")
    new_letters  = []
    for l in letter:
        new_letters.append('<p style="text-indent: 40px">'+l+"</p>")
    letter = "".join(new_letters)
    col1.write(letter, unsafe_allow_html=True)

    start = letter_data.iloc[0]["start_page"]
    end = letter_data.iloc[0]["end_page"]

    image_list = start, end
    all_images = []
    for i in range(start, end+1):
        all_images.append(i)

    #Scriptural References
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


    scrip_expander = st.sidebar.expander(f"Scripture References ({len(scrip_refs)})")
    refs_html = "<br>".join(scrip_refs)
    scrip_expander.write(refs_html, unsafe_allow_html=True)

    col2.header(f"Letter {ep_file} Image(s)")
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

    letter = letter.split("\n\n")
    new_letters  = []
    for l in letter:
        new_letters.append('<p style="text-indent: 40px">'+l+"</p>")
    letter = "".join(new_letters)
    st.write(letter, unsafe_allow_html=True)



elif options == "NER Mode":
    # # add_selectbox = st.selectbox("Select Letter", letter_nums)
    # ep_file = add_selectbox.split(".")[1].strip()
    # grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    # with open (grab_file, "r", encoding="utf-8") as f:
    #     letter = f.read()
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
            if ent.text not in found_places:
                found_places.append(ent.text)
    found_people.sort()
    found_groups.sort()
    found_places.sort()

    person_expander = st.sidebar.expander(f"Found People ({len(found_people)})")
    person_html = "<br>".join(found_people)
    person_expander.write(person_html, unsafe_allow_html=True )

    group_expander = st.sidebar.expander(f"Found Groups ({len(found_groups)})")
    group_html = "<br>".join(found_groups)
    group_expander.write(group_html, unsafe_allow_html=True )

    place_expander = st.sidebar.expander(f"Found Places  ({len(found_places)})")
    place_html = "<br>".join(found_places)
    place_expander.write(place_html, unsafe_allow_html=True )


elif options == "Alcuin's Epistolary Network":
    with open ("data/alcuin_all_letters.html", 'r', encoding='utf-8') as f:
        source_code = f.read()
    st.write("In this Mode, all Light Blue Nodes are people, while all Red Nodes are letters. If you put your mouse over a node, you can see all the other nodes to which it is connected. In this network graph, we can see the many inter-personal relationships Alcuin had with intellectuals across Europe and Britain via his vast epistolary network.")
    components.html(source_code, height = 1200,width=1000)

elif options == "Textual Network":
    st.write("In this Mode, all Light Blue Nodes are manuscripts in which letters appear, while all Red Nodes are letters. If you put your mouse over a node, you can see all the other nodes to which it is connected. This map entirely captures the Donald Bullough thesis about Alcuin's letters surviving in different places across time and space. The tight clusters indicate a concentration of letters appearing in similar and overlapping manuscripts, such as the Tours manuscrips and the Salzburg manuscripts.")
    with open ("data/alcuin_textual_network.html", 'r', encoding='utf-8') as f:
        source_code = f.read()
    components.html(source_code, height = 1200,width=1500)

elif options == "Database Mode":
    st.write("Welcome to the database. Here you can search and find all letters that reference a specific person or you can find all letters that are preserved in a specific manuscript. You can select multiple options. If Strict Search On is selected, all conditions must be True for a result to populate. If it is not selected, then any of the conditions can be true.")
    st.header("Database Mode")
    df = pd.read_csv("data/dap_dataset.csv")
    df = df.fillna(" ")
    manuscripts = list(df["valid_mss"])

    all_mss = []
    for ms in manuscripts:
        ms = ms.split(",")
        for m in ms:
            m = m.strip()
            if m not in all_mss and m != "":
                all_mss.append(m)

    people = list(df["pase_refs"])

    all_people = []
    for p in people:
        if p != " ":
            ps = literal_eval(p)
            for m in ps:
                m = m.strip()
                if m not in all_people and m != "":
                    all_people.append(m)
    all_people.sort()
    all_mss.sort()
    form_options = st.form("Query Form")
    strict_box = form_options.checkbox("Strict Search On")
    mss_select = form_options.multiselect(f"Manuscript ({len(all_mss)})", all_mss)
    people_select = form_options.multiselect(f"People ({len(all_people)})", all_people)
    form_options.form_submit_button()


    if strict_box == False:
        cond1  = [any(y in mss_select for y in x ) for x in df['valid_mss'].str.split(", ")]
        main_cond = cond1
        if len(people_select) > 0:
            cond2  = [x for x in df['pase_refs'].str.contains("|".join(people_select))]
            main_cond = cond1
            i=0
            for c in cond2:
                if c == True:
                    main_cond[i] = True
                i=i+1

        new_df = df.loc[main_cond, :]
    else:
        import numpy as np
        #https://stackoverflow.com/questions/60932036/check-if-pandas-column-contains-all-elements-from-a-list
        mss_select = set(mss_select)
        cond1 = [x for x in df['valid_mss'].str.split(", ").apply(lambda x: set(mss_select).issubset(x))]
        cond2 = [x for x in df['pase_refs'].apply(lambda x: np.all([*map(lambda l: l in x, people_select)]))]


        main_cond = []
        i=0
        for c in cond2:
            if c == True and cond1[i] == True:
                main_cond.append(True)
            else:
                main_cond.append(False)
            i=i+1
        new_df = df.loc[main_cond, :]
    st.table(new_df)


elif options == "About Project":
    st.write('This project was designed by <a href="https://wjbmattingly.com" target="_blank">William Mattingly</a> as part of a larger project, <a href="https://pythonhumanities.com" target="_blank">PythonHumanities.com</a> to provide the letters of Alcuin in raw text alongside their MGH editions with named entity-recognition and Scriptural and Patristic sources extracted from the text. It is currently in Alpha. The data needs to be manually validated still.<br><br>For each letter available, we have linked to letter to the <a href="https://pase.ac.uk/" target="_blank">PASE (Prosopography of Anglo-Saxon England)</a> dataset of Alcuin\'s letters which include all individuals cited in or recipients of the letters. Each individual has their unique PASE-ID and is hyper-linked to the PASE database.', unsafe_allow_html=True)

elif options == "Sources for Data":
    st.write("All Persons, Prosopography of Anglo-Saxon England, http://www.pase.ac.uk, accessed 15 August 2021.")






#
