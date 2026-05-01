import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    conn = duckdb.connect('rental_data/gold/dev.duckdb')
    data = {
        'trend': conn.execute("SELECT * FROM rent_trend").df(),
        'rankings': conn.execute("SELECT * FROM nb_rent_ranking").df(),
        'listings': conn.execute("SELECT * FROM nb_listings").df(),
        'furnished': conn.execute("SELECT * FROM furnished_impact").df(),
        'pct': conn.execute("SELECT * FROM furnished_percentage").df()
    }
    conn.close()
    return data


def main():
    st.set_page_config(layout="wide")
    st.title("Rental Market Analysis")

    data = load_data()

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rent Trend")
        fig = px.line(data['trend'], x='quarter', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')


    with col2:
        st.subheader("Properties per Neighborhood")
        fig = px.bar(data['listings'].head(10), x='neighborhood', y='total_properties')
        st.plotly_chart(fig, width='stretch')
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Top Neighborhoods by Rent")
        fig = px.bar(data['rankings'].head(10), x='neighborhood', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("Furnished Premium")
        fig = px.bar(data['furnished'], x='furnishing_category', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')

    with col3:
        st.subheader("Market Composition")
        fig = px.pie(data['pct'], values='percentage', names='percentage')
        st.plotly_chart(fig, width='stretch')

if __name__ == "__main__":
    main()
