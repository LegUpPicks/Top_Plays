import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sports Betting Analytics",
    page_icon="",
    layout="wide"
)

# Display logo
st.image("legup.png", width=200)

# Title
st.title("Top Plays Analysis")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("top_plays.csv")
    # Clean up the data - remove rows with missing MASTER values
    df = df[df['MASTER'].notna()].copy()
    # Convert DATE to datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    return df

try:
    df = load_data()

    # Overall Statistics Section
    st.header("Overall Statistics")

    total_plays = len(df)
    wins = len(df[df['MASTER'] == 'W'])
    losses = len(df[df['MASTER'] == 'L'])
    pushes = len(df[df['MASTER'] == 'P'])

    total_units_risked = df['UNITS_OUT'].sum()
    total_units_won = df['UNITS_IN'].sum()
    net_units = total_units_won - total_units_risked
    roi = (net_units / total_units_risked * 100) if total_units_risked > 0 else 0
    win_rate = (wins / total_plays * 100) if total_plays > 0 else 0

    # First row: Total Plays, Wins, Losses, Pushes
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Plays", total_plays)
    with col2:
        st.metric("Wins", wins)
    with col3:
        st.metric("Losses", losses)
    with col4:
        st.metric("Pushes", pushes)

    # Second row: Win Rate, ROI, Net Units (aligned with row above)
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col6:
        st.metric("ROI", f"{roi:+.2f}%")
    with col7:
        st.metric("Net Units", f"{net_units:+.2f}")

    st.markdown("---")

    # Analyst Statistics Section
    st.header("Analyst Statistics")

    # Calculate statistics by member
    member_stats = []

    for member in df['MEMBER'].unique():
        member_df = df[df['MEMBER'] == member]

        m_total = len(member_df)
        m_wins = len(member_df[member_df['MASTER'] == 'W'])
        m_losses = len(member_df[member_df['MASTER'] == 'L'])
        m_pushes = len(member_df[member_df['MASTER'] == 'P'])

        m_units_risked = member_df['UNITS_OUT'].sum()
        m_units_won = member_df['UNITS_IN'].sum()
        m_net_units = m_units_won - m_units_risked
        m_roi = (m_net_units / m_units_risked * 100) if m_units_risked > 0 else 0
        m_win_rate = (m_wins / m_total * 100) if m_total > 0 else 0

        member_stats.append({
            'Analyst': member,
            'Total Plays': m_total,
            'Wins': m_wins,
            'Losses': m_losses,
            'Pushes': m_pushes,
            'Win Rate': f"{m_win_rate:.1f}%",
            'Units Risked': f"{m_units_risked:.2f}",
            'Units Won': f"{m_units_won:.2f}",
            'Net Units': f"{m_net_units:+.2f}",
            'ROI': f"{m_roi:+.2f}%"
        })

    member_stats_df = pd.DataFrame(member_stats)

    # Sort by Net Units (descending)
    member_stats_df['Net Units Numeric'] = member_stats_df['Net Units'].apply(lambda x: float(x))
    member_stats_df = member_stats_df.sort_values('Net Units Numeric', ascending=False)
    member_stats_df = member_stats_df.drop('Net Units Numeric', axis=1)

    # Display member statistics table
    st.dataframe(
        member_stats_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            'Analyst': st.column_config.TextColumn('Analyst', width='medium'),
            'Total Plays': st.column_config.NumberColumn('Total Plays', width='small'),
            'Wins': st.column_config.NumberColumn('Wins', width='small'),
            'Losses': st.column_config.NumberColumn('Losses', width='small'),
            'Pushes': st.column_config.NumberColumn('Pushes', width='small'),
            'Win Rate': st.column_config.TextColumn('Win Rate', width='small'),
            'Units Risked': st.column_config.TextColumn('Units Risked', width='medium'),
            'Units Won': st.column_config.TextColumn('Units Won', width='medium'),
            'Net Units': st.column_config.TextColumn('Net Units', width='medium'),
            'ROI': st.column_config.TextColumn('ROI', width='small')
        }
    )

    st.markdown("---")

    # Recent Plays Section
    st.header("Recent Plays")

    # Show last 10 plays
    recent_plays = df.sort_values('DATE', ascending=False).head(10)

    display_df = recent_plays[['DATE', 'PLAY', 'ODDS', 'MEMBER', 'MASTER', 'UNITS_OUT', 'UNITS_IN']].copy()
    display_df['DATE'] = display_df['DATE'].dt.strftime('%b %d, %Y')

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            'DATE': st.column_config.TextColumn('Date', width='small'),
            'PLAY': st.column_config.TextColumn('Play', width='large'),
            'ODDS': st.column_config.TextColumn('Odds', width='small'),
            'MEMBER': st.column_config.TextColumn('Analyst', width='medium'),
            'MASTER': st.column_config.TextColumn('Result', width='small'),
            'UNITS_OUT': st.column_config.NumberColumn('Units Risked', width='small', format="%.2f"),
            'UNITS_IN': st.column_config.NumberColumn('Units Won', width='small', format="%.2f")
        }
    )

    # Detailed Analyst View
    st.markdown("---")
    st.header("Detailed Analyst View")

    selected_member = st.selectbox("Select an analyst to view their plays:", df['MEMBER'].unique())

    if selected_member:
        member_plays = df[df['MEMBER'] == selected_member].sort_values('DATE', ascending=False)

        # Analyst summary
        m_df = member_plays
        m_total = len(m_df)
        m_wins = len(m_df[m_df['MASTER'] == 'W'])
        m_losses = len(m_df[m_df['MASTER'] == 'L'])
        m_units_risked = m_df['UNITS_OUT'].sum()
        m_units_won = m_df['UNITS_IN'].sum()
        m_net = m_units_won - m_units_risked
        m_roi = (m_net / m_units_risked * 100) if m_units_risked > 0 else 0
        m_win_rate = (m_wins / m_total * 100) if m_total > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"{selected_member} - Total Plays", m_total)
        with col2:
            st.metric("Win Rate", f"{m_win_rate:.1f}%")
        with col3:
            st.metric("Net Units", f"{m_net:+.2f}")
        with col4:
            st.metric("ROI", f"{m_roi:+.2f}%")

        # Display all plays for the member
        st.subheader(f"All Plays by {selected_member}")

        display_member_df = member_plays[['DATE', 'PLAY', 'ODDS', 'MASTER', 'UNITS_OUT', 'UNITS_IN']].copy()
        display_member_df['DATE'] = display_member_df['DATE'].dt.strftime('%b %d, %Y')
        display_member_df['Net'] = display_member_df['UNITS_IN'] - display_member_df['UNITS_OUT']

        st.dataframe(
            display_member_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                'DATE': st.column_config.TextColumn('Date', width='small'),
                'PLAY': st.column_config.TextColumn('Play', width='large'),
                'ODDS': st.column_config.TextColumn('Odds', width='small'),
                'MASTER': st.column_config.TextColumn('Result', width='small'),
                'UNITS_OUT': st.column_config.NumberColumn('Units Risked', width='small', format="%.2f"),
                'UNITS_IN': st.column_config.NumberColumn('Units Won', width='small', format="%.2f"),
                'Net': st.column_config.NumberColumn('Net', width='small', format="%+.2f")
            }
        )

except FileNotFoundError:
    st.error("Error: top_plays.csv file not found. Please ensure the file is in the same directory as this app.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
