import streamlit as st
import glob
import json
import spacy_streamlit

spacy_model = "models/latin_ruler_backup"

visualizers = ["entity_ruler"]

st.title("The Digital Alcuin Project")

st.sidebar.header("Choose App Task")
options = st.sidebar.selectbox("Select Mode",
                    ("Letter Mode", "NER Mode", "Side-by-Side Mode"))

with open ("data/letter_page_spans.json", "r") as f:
    page_spans = json.load(f)

files = glob.glob("data/cleaned_letters/*txt")
letter_nums = []
for file in files:
    file = file.split("cleaned_letters_")[1].replace(".txt", "")
    ep = f"Ep. {file}"
    letter_nums.append(ep)
add_selectbox = st.selectbox("Select Letter", letter_nums)

if options == "Side-by-Side Mode":
    col1, col2 = st.beta_columns(2)
    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()


    clean_ep = ep_file.lstrip("0")
    col1.header(f"Letter {clean_ep} Text")

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
    ep_file = add_selectbox.split(".")[1].strip()
    grab_file = f"data/cleaned_letters/cleaned_letters_{ep_file}.txt"
    with open (grab_file, "r", encoding="utf-8") as f:
        letter = f.read()
    clean_ep = ep_file.lstrip("0")
    st.header(f"Letter {clean_ep} Text")
    st.write(letter)


if options == "NER Mode":
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








#
