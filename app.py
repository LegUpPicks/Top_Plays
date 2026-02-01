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

# Title and date filter will be added after data loads

# Load data from Google Sheet
SHEET_ID = "1U1gt5RsN3kOC6ZWQidpmF56wW3qAhwLfPrMJib-WiNg"
SHEET_NAME = "MASTER"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=300)  # Cache for 5 minutes to allow refreshing from sheet
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Clean up the data - remove rows with missing MASTER values
    df = df[df['MASTER'].notna()].copy()
    # Convert DATE to datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    return df

try:
    df = load_data()

    # Title and Date Filter (same row)
    min_date = df['DATE'].min().date()
    max_date = df['DATE'].max().date()

    title_col, _, filter_col1, filter_col2 = st.columns([3, 1, 1, 1])

    with title_col:
        st.title("Top Plays Analysis")
    with filter_col1:
        start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    with filter_col2:
        end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

    st.markdown("---")

    # Apply date filter
    df = df[(df['DATE'].dt.date >= start_date) & (df['DATE'].dt.date <= end_date)]

    # Top 5 Analysts Statistics Section (by Net Units)
    st.header("Top 5 Analysts Statistics (by Net Units)")

    # Calculate net units per analyst and get top 5
    analyst_net_units = df.groupby('MEMBER').apply(
        lambda x: x['UNITS_IN'].sum() - x['UNITS_OUT'].sum()
    ).sort_values(ascending=False)
    top5_analysts = analyst_net_units.head(5).index.tolist()

    # Filter data to only top 5 analysts
    top5_df = df[df['MEMBER'].isin(top5_analysts)]

    top5_total_plays = len(top5_df)
    top5_wins = len(top5_df[top5_df['MASTER'] == 'W'])
    top5_losses = len(top5_df[top5_df['MASTER'] == 'L'])
    top5_pushes = len(top5_df[top5_df['MASTER'] == 'P'])

    top5_units_risked = top5_df['UNITS_OUT'].sum()
    top5_units_won = top5_df['UNITS_IN'].sum()
    top5_net_units = top5_units_won - top5_units_risked
    top5_roi = (top5_net_units / top5_units_risked * 100) if top5_units_risked > 0 else 0
    top5_win_rate = (top5_wins / top5_total_plays * 100) if top5_total_plays > 0 else 0

    # First row: Total Plays, Wins, Losses, Pushes
    t5_col1, t5_col2, t5_col3, t5_col4 = st.columns(4)

    with t5_col1:
        st.metric("Total Plays", top5_total_plays)
    with t5_col2:
        st.metric("Wins", top5_wins)
    with t5_col3:
        st.metric("Losses", top5_losses)
    with t5_col4:
        st.metric("Pushes", top5_pushes)

    # Second row: Win Rate, ROI, Net Units (aligned with row above)
    t5_col5, t5_col6, t5_col7, t5_col8 = st.columns(4)

    with t5_col5:
        st.metric("Win Rate", f"{top5_win_rate:.1f}%")
    with t5_col6:
        st.metric("ROI", f"{top5_roi:+.2f}%")
    with t5_col7:
        st.metric("Net Units", f"{top5_net_units:+.2f}")

    st.markdown("---")

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

except Exception as e:
    st.error(f"Error loading data from Google Sheet: {str(e)}")
    st.info("Please ensure the Google Sheet is publicly accessible (Anyone with the link can view).")
