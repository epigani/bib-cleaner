import streamlit as st
import re

def preprocess_bib_file(content):
    """
    Preprocess the content of one or more .bib files to remove duplicate citation keys and sort the entries.
    """
    lines = content.splitlines()
    unique_keys = {}
    processed_entries = []
    current_entry = []
    inside_entry = False
    current_key = None

    # Process each line to format entries properly
    for line in lines:
        if line.strip().startswith('@'):
            if current_entry:  # Process the previous entry if it's complete
                if current_key and current_key not in unique_keys:
                    unique_keys[current_key] = True
                    processed_entries.append('\n'.join(current_entry) + '\n')
                elif current_key:
                    st.warning(f"Duplicate entry removed: {current_key}")
            inside_entry = True
            current_entry = [line]
            match = re.match(r'@.*?\{(.*?),', line)
            if match:
                current_key = match.group(1).strip()
        elif inside_entry and line.strip() == '}':
            current_entry.append(line)
            inside_entry = False
            # The entry ends here; it will be processed in the next iteration
        elif inside_entry:
            current_entry.append(line)

    # Append the last entry if not a duplicate
    if current_entry and current_key and current_key not in unique_keys:
        processed_entries.append('\n'.join(current_entry) + '\n')

    # Sort entries alphabetically
    entries_sorted = sorted(processed_entries, key=lambda x: x.split('{', 1)[1].split(',', 1)[0] if '{' in x and ',' in x.split('{', 1)[1] else '')

    # Add alphabet section headers and separate entries with a new line
    sorted_entries = []
    current_letter = None
    for entry in entries_sorted:
        first_letter = entry.split('{', 1)[1][0].upper() if '{' in entry else 'Unknown'
        if first_letter != current_letter:
            current_letter = first_letter
            sorted_entries.append(f"\n%%%% {current_letter} %%%%\n")
        sorted_entries.append(entry + '\n')

    return ''.join(sorted_entries)

def main():
    st.title("BibTeX File Cleaner and Sorter")
    uploaded_files = st.file_uploader("Choose .bib files", type="bib", accept_multiple_files=True)
    if uploaded_files:
        combined_content = ""
        for uploaded_file in uploaded_files:
            # Read each file and combine
            file_content = uploaded_file.getvalue().decode("utf-8")
            combined_content += file_content + "\n"

        if st.button("Process Files"):
            processed_content = preprocess_bib_file(combined_content)
            st.download_button("Download Processed File", processed_content, "processed.bib", "text/plain")

if __name__ == "__main__":
    main()


# import streamlit as st
# import re

# def preprocess_bib_file(content):
#     """
#     Preprocess the content of a .bib file to remove duplicate citation keys and sort the entries.
#     """
#     lines = content.splitlines()
#     unique_keys = {}
#     processed_entries = []
#     current_entry = []
#     inside_entry = False
#     current_key = None

#     # Process each line to format entries properly
#     for line in lines:
#         if line.strip().startswith('@'):
#             if current_entry:  # Process the previous entry if it's complete
#                 if current_key and current_key not in unique_keys:
#                     unique_keys[current_key] = True
#                     processed_entries.append('\n'.join(current_entry) + '\n')
#                 elif current_key:
#                     st.warning(f"Duplicate entry removed: {current_key}")
#             inside_entry = True
#             current_entry = [line]
#             match = re.match(r'@.*?\{(.*?),', line)
#             if match:
#                 current_key = match.group(1).strip()
#         elif inside_entry and line.strip() == '}':
#             current_entry.append(line)
#             inside_entry = False
#             # The entry ends here; it will be processed in the next iteration
#         elif inside_entry:
#             current_entry.append(line)

#     # Append the last entry if not a duplicate
#     if current_entry and current_key and current_key not in unique_keys:
#         processed_entries.append('\n'.join(current_entry) + '\n')

#     # Safe sorting: Ensure that every entry has a valid sort key
#     entries_sorted = sorted(processed_entries, key=lambda x: x.split('{', 1)[1].split(',', 1)[0] if '{' in x and ',' in x.split('{', 1)[1] else '')

#     # Add alphabet section headers and separate entries with a new line
#     sorted_entries = []
#     current_letter = None
#     for entry in entries_sorted:
#         first_letter = entry.split('{', 1)[1][0].upper() if '{' in entry else 'Unknown'
#         if first_letter != current_letter:
#             current_letter = first_letter
#             sorted_entries.append(f"\n%%%% {current_letter} %%%%\n")
#         sorted_entries.append(entry + '\n')

#     return ''.join(sorted_entries)

# def main():
#     st.title("BibTeX File Cleaner and Sorter")
#     uploaded_file = st.file_uploader("Choose a .bib file", type="bib")
#     if uploaded_file is not None:
#         content = uploaded_file.getvalue().decode("utf-8")
#         if st.button("Process File"):
#             processed_content = preprocess_bib_file(content)
#             st.download_button("Download Processed File", processed_content, "processed.bib", "text/plain")

# if __name__ == "__main__":
#     main()
