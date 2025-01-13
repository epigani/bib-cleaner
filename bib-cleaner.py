import streamlit as st
import re

def preprocess_bib_file(content):
    lines = content.splitlines()
    unique_keys = {}
    duplicate_entries = {}
    processed_entries = []
    current_entry = []
    inside_entry = False
    current_key = None

    for line in lines:
        if line.strip().startswith('@'):
            if current_entry:  # End of the previous entry
                if current_key:
                    if current_key in unique_keys:
                        if current_key in duplicate_entries:
                            duplicate_entries[current_key].append('\n'.join(current_entry))
                        else:
                            duplicate_entries[current_key] = [unique_keys[current_key], '\n'.join(current_entry)]
                    else:
                        unique_keys[current_key] = '\n'.join(current_entry)
                        processed_entries.append(unique_keys[current_key])
            current_entry = [line]
            match = re.match(r'@.*?\{(.*?),', line)
            if match:
                current_key = match.group(1).strip()
        elif inside_entry and line.strip() == '}':
            current_entry.append(line)
            inside_entry = False
        elif inside_entry:
            current_entry.append(line)
        else:
            if line.strip():
                processed_entries.append(line)  # add non-entry content as is

    sorted_entries = sorted(processed_entries, key=lambda x: x.split('{', 1)[1].split(',', 1)[0])

    return sorted_entries, duplicate_entries

def display_duplicates(duplicate_entries):
    for key, entries in duplicate_entries.items():
        if len(entries) > 5:
            with st.expander(f"{len(entries)} duplicates for key {key} (click to expand)"):
                st.write("\n\n".join(entries))
        else:
            st.write(f"{len(entries)} duplicates for key {key}:")
            st.write("\n\n".join(entries))

def main():
    st.title("BibTeX File Cleaner and Sorter")
    uploaded_files = st.file_uploader("Choose .bib files", type="bib", accept_multiple_files=True)
    if uploaded_files:
        combined_content = ""
        for uploaded_file in uploaded_files:
            file_content = uploaded_file.getvalue().decode("utf-8")
            combined_content += file_content + "\n"

        if st.button("Process Files"):
            processed_content, duplicate_entries = preprocess_bib_file(combined_content)
            display_duplicates(duplicate_entries)
            processed_content = "\n".join(processed_content)
            st.download_button("Download Processed File", processed_content, "processed.bib", "text/plain")

if __name__ == "__main__":
    main()