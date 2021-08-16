import streamlit as st
import glob
import json
import spacy_streamlit
import streamlit.components.v1 as components

spacy_model = "models/latin_ruler_backup"

visualizers = ["entity_ruler"]

st.title("The Digital Alcuin Project")

st.sidebar.header("Choose App Task")
options = st.sidebar.selectbox("Select Mode",
                    ("Letter Mode", "NER Mode", "Side-by-Side Mode", "Alcuin's Epistolary Network", "Sources for Data"))

with open ("data/letter_page_spans.json", "r") as f:
    page_spans = json.load(f)

with open ("data/letter_header.json", "r") as f:
    headers = json.load(f)

with open ("data/letter_people.json", "r") as f:
    letter_people = json.load(f)

with open ("data/pase_keys.json", "r") as f:
    pase_keys = json.load(f)

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

    st.header(f"Letter {clean_ep} Text")
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


if options == "NER Mode":
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


if options == "Alcuin's Epistolary Network":
    with open ("data/alcuin_all_letters.html", 'r', encoding='utf-8') as f:
        source_code = f.read()
    components.html(source_code, height = 1200,width=1000)


if options == "Sources for Data":
    st.write("All Persons, Prosopography of Anglo-Saxon England, http://www.pase.ac.uk, accessed 15 August 2021.")





#
