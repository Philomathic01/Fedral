import streamlit as st
import requests
import datetime


st.markdown("<h1 style='color: #4CAF50; text-align: center;'>Federal Register API Explorer</h1>", unsafe_allow_html=True)


st.markdown("### 🚀 Explore Federal Register Documents")
st.markdown("Use this tool to interact with the Federal Register API and retrieve documents based on various parameters. Customize your search criteria below and click **Submit** to view results.")


with st.form(key='api_form'):
    st.markdown("#### 🔍 **Search Parameters**")
    

    include_term = st.checkbox("Include Search Term 📝", value=True)
    if include_term:
        term = st.text_input("Search Term", value="Hipaa")

    include_section = st.checkbox("Include Section 🏛️", value=True)
    if include_section:
        section = st.selectbox("Section", ["Health-and-public-welfare"])

    include_topic = st.checkbox("Include Topic 🏥", value=True)
    if include_topic:
        topic = st.selectbox("Topic", ["health-care"])

    include_cfr_title = st.checkbox("Include CFR Title 📖", value=True)
    if include_cfr_title:
        cfr_title = st.selectbox("CFR Title", [20])

    include_cfr_part = st.checkbox("Include CFR Part 📃", value=True)
    if include_cfr_part:
        cfr_part = st.number_input("CFR Part", min_value=0, value=14)

    include_significant = st.checkbox("Include Significant Flag 🔑", value=True)
    if include_significant:
        significant = st.selectbox("Significant", [1, 0])

    include_dates = st.checkbox("Include Publication Date Range 📅", value=True)
    if include_dates:
        start_date = st.date_input("Start Publication Date", value=datetime.date(2024, 8, 30))
        end_date = st.date_input("End Publication Date", value=datetime.date(2024, 9, 28))

    include_effective_year = st.checkbox("Include Effective Date Year 🗓️", value=True)
    if include_effective_year:
        effective_year = st.number_input("Effective Date Year", min_value=1984, value=2024)
    
    include_Publishing_year = st.checkbox("Include Publishing  Year 🗓️", value=True)
    if include_Publishing_year:
        Publishing_year = st.number_input("Publishing  Year", min_value=1984, value=2024)
    
    per_page = st.number_input("Results per Page 📄", min_value=1, max_value=1000)

    submit_button = st.form_submit_button(label="🚀 Submit Search")


if submit_button:
    
    api_url = "https://www.federalregister.gov/api/v1/documents.json"

    params = {
        "per_page": per_page,
        "order": "relevance"
    }

    # Include each parameter only if the corresponding checkbox is selected
    if include_term:
        params["conditions[term]"] = term

    if include_section:
        params["conditions[sections][]"] = section

    if include_topic:
        params["conditions[topics][]"] = topic

    if include_cfr_title:
        params["conditions[cfr][title]"] = cfr_title

    if include_cfr_part:
        params["conditions[cfr][part]"] = cfr_part

    if include_significant:
        params["conditions[significant]"] = significant

    if include_dates:
        params["conditions[publication_date][gte]"] = start_date
        params["conditions[publication_date][lte]"] = end_date

    if include_effective_year:
        params["conditions[effective_date][year]"] = effective_year
    
    if include_Publishing_year:
        params["conditions[publication_date][year]"] = Publishing_year

    # Fetch results from the API
    response = requests.get(api_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        if 'results' in data:
            st.markdown(f"<h3 style='color: #4CAF50;'>Found {len(data['results'])} Results</h3>", unsafe_allow_html=True)

            # Display each result in a styled container
            for document in data['results']:
                st.markdown("<div style='border: 2px solid #4CAF50; padding: 10px; margin: 10px 0; border-radius: 5px;'>", unsafe_allow_html=True)
                st.markdown(f"**Title:** {document.get('title', 'N/A')}")
                st.markdown(f"**Publication Date:** {document.get('publication_date', 'N/A')}")
                st.markdown(f"**abstract:** {document.get('abstract', 'N/A')}")
                st.markdown(f"**Details URL:** [Link]({document.get('html_url', 'N/A')})")
                st.markdown(f"**PDF URL:** [Link]({document.get('pdf_url','N/A')})")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No 'results' key found in the response.")
    else:
        st.error(f"Failed to fetch data. Status Code: {response.status_code}")
        st.write("Error response:", response.text)
