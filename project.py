import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(layout="wide", page_title="T20 World Cup Analysis")

#  Step 1: Add  CSS and HTML
# (No changes in this section)
st.markdown("""
<style>
    /* Main background color for the app */
    .stApp {
        background-color: #2E2E2E; /* Charcoal background */
        color: #E0E0E0;          /* Light text for dark background */
    }
    
    /* Style for the sidebar */
    [data-testid="stSidebar"] {
        background-color: #252525; /* Darker sidebar */
        border-right: 1px solid #444444;
    }

    /* Style for the KPI cards */
    .kpi-card {
        background-color: #252525;      /* Card background */
        border-radius: 10px;            /* Rounded corners */
        padding: 20px;                  /* Space inside the card */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Subtle shadow */
        text-align: center;             /* Center-align text */
        margin-bottom: 15px;            /* Space between cards */
    }
    .kpi-title {
        font-size: 16px;
        color: #AAAAAA;                /* Light grey for title */
        font-weight: 600;
    }
    .kpi-value {
        font-size: 32px;
        color: #00BFA5;                /* Premium Teal/Aqua color */
        font-weight: bold;
    }
    
    /* Style for chart containers (Seaborn doesn't need this, but good to have) */
    [data-testid="stDeckGlJsonChart"] { /* Target st.pyplot */
        background-color: #252525;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit header, footer, and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

#  1.5. SEABORN & MATPLOTLIB  CONFIG 
# (No changes in this section)
sns.set_theme(style="darkgrid")
plt.rcParams['figure.facecolor'] = '#252525'  
plt.rcParams['axes.facecolor'] = '#252525'    
plt.rcParams['text.color'] = '#E0E0E0'        
plt.rcParams['axes.labelcolor'] = '#E0E0E0'  
plt.rcParams['xtick.color'] = '#E0E0E0'       
plt.rcParams['ytick.color'] = '#E0E0E0'       
plt.rcParams['axes.titlecolor'] = "#10F5D6"  
plt.rcParams['figure.dpi'] = 100              


#  2. DATA LOADING & CLEANING (FROM CSVs) 
# (No changes in this section)
@st.cache_data
def load_data():
    try:
        # Load all datasets (use actual filenames in this workspace)
        batting_df = pd.read_csv("batting_stats_for_icc_mens_t20_world_cup_2024.csv")
        bowling_df = pd.read_csv("bowling_stats_for_icc_mens_t20_world_cup_2024.csv")
        fielding_df = pd.read_csv("fielding_stats_for_icc_mens_t20_world_cup_2024.csv")
        match_df = pd.read_csv("match_results_for_icc_mens_t20_world_cup_2024.csv")
        wk_df = pd.read_csv("wk_stats_for_icc_mens_t20_world_cup_2024.csv")

        
        batting_df['HS'] = batting_df['HS'].astype(str).str.replace('*', '', regex=False)
        bat_num_cols = ['Runs', 'Ave', 'SR', '100', '50', '0', 'HS']
        for col in bat_num_cols:
            batting_df[col] = pd.to_numeric(batting_df[col], errors='coerce').fillna(0)

        
        bowl_num_cols = ['Balls', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ', 'SR']
        for col in bowl_num_cols:
            bowling_df[col] = pd.to_numeric(bowling_df[col], errors='coerce').fillna(0)

        
        match_df = match_df[match_df['Winner'] != 'no result']
        match_df = match_df[match_df['Winner'] != 'tied']
        
        
        fielding_df['Ct'] = pd.to_numeric(fielding_df['Ct'], errors='coerce').fillna(0)
        
        
        wk_cols = ['Dis', 'Ct', 'St']
        for col in wk_cols:
            wk_df[col] = pd.to_numeric(wk_df[col], errors='coerce').fillna(0)

        return batting_df, bowling_df, fielding_df, match_df, wk_df
    
    except FileNotFoundError:
        st.error("One or more CSV files not found. Please make sure all 5 files are in the same directory.")
        return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())


batting_stats, bowling_stats, fielding_stats, match_results, wk_stats = load_data()


all_players = sorted(list(set(batting_stats['Player'].unique()) | set(bowling_stats['Player'].unique())))

# 3. SIDEBAR NAVIGATION
# --- START OF MODIFIED SECTION ---
st.sidebar.title("Dashboard Menu")
page = st.sidebar.radio(
    "Select your analysis",
    ["🏆 Tournament Summary", 
     "🏏 Batting Analysis", 
     "⚾ Bowling Analysis", 
     "🧤 Fielding & WK Analysis", 
     "👤 Player Analysis"] 
)


st.sidebar.markdown("---")
# Replaced captions with centered markdown for a symmetrical look
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <small>Created by<br><b>Ankush Bhandari & Harris</b></small>
        <br><br>
        <small>Made using 🐍 Python, Streamlit,<br>Numpy, & Seaborn</small>
    </div>
    """,
    unsafe_allow_html=True
)
# --- END OF MODIFIED SECTION ---


#  4. PAGE: TOURNAMENT SUMMARY 
#  Step 4: Build the "Tournament Summary" Page 
#  Updated 'if' statement to match the new emoji label
if page == "🏆 Tournament Summary" and not batting_stats.empty and not bowling_stats.empty:
    st.title("T20 World Cup - Tournament Summary")
    st.markdown("A top-level overview of the tournament stats.")

    # --- KPI Cards ---
    st.markdown("### Tournament Highlights")
    total_runs = int(batting_stats['Runs'].sum())
    total_wickets = int(bowling_stats['Wkts'].sum())
    total_matches = len(match_results)
    total_fifties = int(batting_stats['50'].sum())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total Runs</div><div class="kpi-value">{total_runs:,}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total Wickets</div><div class="kpi-value">{total_wickets:,}</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total Matches</div><div class="kpi-value">{total_matches}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total 50s</div><div class="kpi-value">{total_fifties}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    #  Step 5: Create Visualizations with Seaborn 
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Run Scorers")
        top_5_runs = batting_stats.nlargest(5, 'Runs')
        
        # Create Matplotlib figure
        fig_runs, ax = plt.subplots()
        # Create Seaborn bar plot
        sns.barplot(data=top_5_runs, 
                    x='Runs', 
                    y='Player', 
                    palette=["#4C8FFB"], 
                    ax=ax)
        ax.set_title("Top 5 Run Scorers")
        ax.set_xlabel("Total Runs")
        ax.set_ylabel("Player")
        plt.tight_layout()
        st.pyplot(fig_runs)
        
    with col2:
        st.subheader("Top 5 Wicket Takers")
        top_5_wickets = bowling_stats.nlargest(5, 'Wkts')
        
        fig_wickets, ax = plt.subplots()
        sns.barplot(data=top_5_wickets, 
                    x='Wkts', 
                    y='Player', 
                    palette=["#00BFA5"], 
                    ax=ax)
        ax.set_title("Top 5 Wicket Takers")
        ax.set_xlabel("Total Wickets")
        ax.set_ylabel("Player")
        plt.tight_layout()
        st.pyplot(fig_wickets)

    #  Team Wins Graph 
    st.subheader("Matches Won by Team (Top 10)")
    team_wins = match_results['Winner'].value_counts().nlargest(10).reset_index()
    team_wins.columns = ['Team', 'Wins']
    
    fig_wins, ax = plt.subplots()
   
    colors = sns.color_palette("coolwarm", len(team_wins))
    
    # Create the pie chart
    wedges, texts, autotexts = ax.pie(team_wins['Wins'], 
                                      labels=team_wins['Team'], 
                                      autopct='%1.1f%%', 
                                      colors=colors, 
                                      startangle=90, 
                                      pctdistance=0.85,
                                      textprops={'color': 'white'})
    
    
    centre_circle = plt.Circle((0,0),0.70,fc='#252525')
    fig_wins.gca().add_artist(centre_circle)
    
    ax.set_title("Team Win Distribution (Top 10)")
    ax.axis('equal') 
    plt.tight_layout()
    st.pyplot(fig_wins)

#  5. PAGE: BATTING ANALYSIS 
#  Updated 'elif' statement to match the new emoji label
elif page == "🏏 Batting Analysis" and not batting_stats.empty:
    st.title("Batting Analysis")
    st.markdown("Detailed batting statistics and player comparisons.")

    #  Scatter Plot: Ave vs SR 
    st.subheader("Average vs. Strike Rate (Min. 50 Runs)")
    filtered_batters = batting_stats[batting_stats['Runs'] >= 50]
    
    fig_scatter, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_batters, 
                    x='Ave', 
                    y='SR',
                    size='Runs',
                    hue='Team',
                    palette='bright', 
                    sizes=(20, 500), 
                    ax=ax)
    ax.set_title("Player Performance (Avg vs. SR)")
    
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig_scatter)

    #  Bar Chart: Top 10 High Scores 
    st.subheader("Top 10 Individual High Scores")
    top_10_hs = batting_stats.nlargest(10, 'HS')
    
    fig_hs, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_hs, 
                x='HS',
                y='Player',
                palette='viridis', 
                ax=ax)
    ax.set_title("Top 10 High Scores")
    ax.set_xlabel("High Score")
    ax.set_ylabel("Player")
    plt.tight_layout()
    st.pyplot(fig_hs)
    
    st.subheader("Full Batting Stats")
    st.dataframe(batting_stats, use_container_width=True)


#  6. PAGE: BOWLING ANALYSIS 
#  Updated 'elif' statement to match the new emoji label
elif page == "⚾ Bowling Analysis" and not bowling_stats.empty:
    st.title("Bowling Analysis")
    st.markdown("Detailed bowling statistics and player comparisons.")

    #  Dot Plot (Scatter): Wickets vs. Economy 
    st.subheader("Wickets vs. Economy Rate (Min. 5 Wickets)")
    filtered_bowlers = bowling_stats[bowling_stats['Wkts'] >= 5]
    
    fig_dot, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_bowlers, 
                    x='Econ', 
                    y='Wkts',
                    size='Ave',
                    hue='Team',
                    palette='bright',
                    sizes=(20, 500), 
                    ax=ax)
    ax.set_title("Player Performance (Wkts vs. Econ)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig_dot)

    #  Histogram: Distribution of Economy Rates 
    st.subheader("Distribution of Economy Rates (Min. 10 Overs)")
    hist_bowlers = bowling_stats[bowling_stats['Balls'] >= 60]
    
    fig_hist, ax = plt.subplots()
    sns.histplot(data=hist_bowlers, 
               x='Econ', 
               bins=20, 
               kde=True, 
               color="#FFD700", 
               ax=ax)
    ax.set_title("Economy Rate Distribution (Min. 10 Overs Bowled)")
    ax.set_xlabel("Economy Rate")
    plt.tight_layout()
    st.pyplot(fig_hist)
    
    st.subheader("Full Bowling Stats")
    st.dataframe(bowling_stats, use_container_width=True)


# 7. PAGE: FIELDING & WICKET-KEEPING ANALYSIS 
#  Updated 'elif' statement to match the new emoji label
elif page == "🧤 Fielding & WK Analysis" and not fielding_stats.empty and not wk_stats.empty:
    st.title("Fielding & Wicket-Keeping Analysis")
    st.markdown("A look at the top performers in the field.")

    col1, col2 = st.columns(2)

    with col1:
        #  Fielding Stats
        st.subheader("Top 10 Fielders (by Catches)")
        top_10_fielders = fielding_stats.nlargest(10, 'Ct')
        
        fig_field, ax = plt.subplots()
        # Create a color palette
        colors = sns.color_palette("YlOrBr_r", len(top_10_fielders))
        
        # Create the pie chart
        wedges, texts, autotexts = ax.pie(top_10_fielders['Ct'], 
                                            labels=top_10_fielders['Player'], 
                                            autopct='%1.1f%%', 
                                            colors=colors, 
                                            startangle=90, 
                                            pctdistance=0.85,
                                            textprops={'color': 'white'})
        
        # Create the "donut hole"
        centre_circle = plt.Circle((0,0),0.70,fc='#252525')
        fig_field.gca().add_artist(centre_circle)
        
        ax.set_title("Top 10 Fielders by Catches")
        ax.axis('equal') 
        plt.tight_layout()
        st.pyplot(fig_field)

    with col2:
        #  Wicket-Keeping Stats 
        st.subheader("Top 10 Wicket-Keepers (by Dismissals)")
        top_10_wk = wk_stats.nlargest(10, 'Dis')
        
        fig_wk_dis, ax = plt.subplots()
    
        colors = sns.color_palette("PuBu_r", len(top_10_wk))

        
        wedges, texts, autotexts = ax.pie(top_10_wk['Dis'], 
                                            labels=top_10_wk['Player'], 
                                            autopct='%1.1f%%', 
                                            colors=colors, 
                                            startangle=90, 
                                            pctdistance=0.85,
                                            textprops={'color': 'white'})
        
        
        centre_circle = plt.Circle((0,0),0.70,fc='#252525')
        fig_wk_dis.gca().add_artist(centre_circle)

        ax.set_title("Top 10 Wicket-Keepers by Dismissals")
        ax.axis('equal') 
        plt.tight_layout()
        st.pyplot(fig_wk_dis)

    st.markdown("<br>", unsafe_allow_html=True)
    
    #  WK Dismissal Breakdown 
    st.subheader("Wicket-Keeper Dismissal Breakdown (Top 10)")
    
    top_10_wk_melted = top_10_wk.melt(
        id_vars=['Player'], 
        value_vars=['Ct', 'St'], 
        var_name='Dismissal Type', 
        value_name='Count'
    )
    
    top_10_wk_melted['Dismissal Type'] = pd.Categorical(top_10_wk_melted['Dismissal Type'], ["Ct", "St"])
    
    fig_wk_stack, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_wk_melted,
                y='Player',
                x='Count',
                hue='Dismissal Type',
                palette=["#4C8FFB", "#00BFA5"], 
                ax=ax,
                order=top_10_wk['Player'] 
                )
    ax.set_title("Dismissal Breakdown (Catches vs. Stumpings)")
    ax.set_xlabel("Count")
    ax.set_ylabel("Player")
    ax.legend(title='Dismissal Type')
    plt.tight_layout()
    st.pyplot(fig_wk_stack)
    
    st.markdown("<br>", unsafe_allow_html=True)


    st.subheader("Full Wicket-Keeping Stats")
    st.dataframe(wk_stats, use_container_width=True)
    
    st.subheader("Full Fielding Stats")
    st.dataframe(fielding_stats, use_container_width=True)


#  8. PAGE: PLAYER ANALYSIS (STAR PLAYERS) 
#  Updated 'elif' statement to match the new emoji label
elif page == "👤 Player Analysis":
    st.title("Player Analysis")
    st.markdown("Select a player for a deep dive or compare multiple players.")

   
    analysis_mode = st.radio(
        "Select View",
        ["Single Player Deep Dive", "Multi-Player Comparison"],
        horizontal=True
    )
    
    st.markdown("---") 
    if analysis_mode == "Single Player Deep Dive":
        # --- Player Selection Dropdown ---
        
        default_index = 0
        if "Virat Kohli" in all_players:
            default_index = all_players.index("Virat Kohli")
            
        selected_player = st.selectbox(
            "Select a Player", 
            all_players, 
            index=default_index
        )
        
        #  Define player dataframes based on selection 
        player_batting = batting_stats[batting_stats['Player'] == selected_player]
        player_bowling = bowling_stats[bowling_stats['Player'] == selected_player]
        player_fielding = fielding_stats[fielding_stats['Player'] == selected_player]
        player_wk = wk_stats[wk_stats['Player'] == selected_player] 

        st.subheader(f"Stats for: {selected_player}")

        # --- Batting Stats ---
        if not player_batting.empty:
            st.markdown("#### Batting")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Runs</div><div class="kpi-value">{player_batting['Runs'].values[0]}</div></div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Batting Avg</div><div class="kpi-value">{player_batting['Ave'].values[0]:.2f}</div></div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Strike Rate</div><div class="kpi-value">{player_batting['SR'].values[0]:.2f}</div></div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">High Score</div><div class="kpi-value">{player_batting['HS'].values[0]}</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("#### Batting\n*No batting stats available for this player.*")

        # --- Bowling Stats ---
        if not player_bowling.empty and player_bowling['Balls'].values[0] > 0:
            st.markdown("#### Bowling")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Wickets</div><div class="kpi-value">{player_bowling['Wkts'].values[0]}</div></div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Bowling Avg</div><div class="kpi-value">{player_bowling['Ave'].values[0]:.2f}</div></div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Economy</div><div class="kpi-value">{player_bowling['Econ'].values[0]:.2f}</div></div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Best Bowling</div><div class="kpi-value">{player_bowling['BBI'].values[0]}</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("#### Bowling\n*No bowling stats available for this player.*")
        
        # --- Fielding Stats ---
        if not player_fielding.empty:
            st.markdown("#### Fielding")
            col1, _, _ = st.columns(3) # Just show catches
            with col1:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Catches</div><div class="kpi-value">{player_fielding['Ct'].values[0]}</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("#### Fielding\n*No fielding stats available for this player.*")

        # --- WICKET-KEEPING STATS TO PLAYER PAGE ---
        if not player_wk.empty:
            st.markdown("#### Wicket-Keeping")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Dismissals</div><div class="kpi-value">{player_wk['Dis'].values[0]}</div></div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Catches (WK)</div><div class="kpi-value">{player_wk['Ct'].values[0]}</div></div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Stumpings</div><div class="kpi-value">{player_wk['St'].values[0]}</div></div>""", unsafe_allow_html=True)
        

    elif analysis_mode == "Multi-Player Comparison":
        st.subheader("Compare Player Stats")

        # --- Multi-Player Selection ---
        default_players = []
        if "Virat Kohli" in all_players:
            default_players.append("Virat Kohli")
        if "Rohit Sharma" in all_players:
            default_players.append("Rohit Sharma")

        selected_players = st.multiselect(
            "Select players to compare",
            all_players,
            default=default_players
        )

        if selected_players:
            bat_compare_df = batting_stats[batting_stats['Player'].isin(selected_players)]
            bowl_compare_df = bowling_stats[bowling_stats['Player'].isin(selected_players)]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Batting Comparison")
                
                if not bat_compare_df.empty:
                    # Runs
                    fig_runs, ax = plt.subplots()
                    sns.barplot(data=bat_compare_df, x='Player', y='Runs', palette="Blues", ax=ax)
                    ax.set_title("Total Runs")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_runs)
                    
                    # Batting Avg
                    fig_avg, ax = plt.subplots()
                    sns.barplot(data=bat_compare_df, x='Player', y='Ave', palette="Greens", ax=ax)
                    ax.set_title("Batting Average")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_avg)

                    # Strike Rate
                    fig_sr, ax = plt.subplots()
                    sns.barplot(data=bat_compare_df, x='Player', y='SR', palette="Oranges", ax=ax) 
                    ax.set_title("Strike Rate")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_sr)
                else:
                    st.warning("No batting data for selected players.")

            with col2:
                st.markdown("#### Bowling Comparison")

                # Filter for players who actually bowled (Wkts > 0 or Balls > 0)
                bowl_compare_df = bowl_compare_df[bowl_compare_df['Balls'] > 0]

                if not bowl_compare_df.empty:
                    # Wickets
                    fig_wkts, ax = plt.subplots()
                    sns.barplot(data=bowl_compare_df, x='Player', y='Wkts', palette="Reds", ax=ax)
                    ax.set_title("Total Wickets")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_wkts)
                    
                    # Economy
                    fig_econ, ax = plt.subplots()
                    sns.barplot(data=bowl_compare_df, x='Player', y='Econ', palette="Purples", ax=ax)
                    ax.set_title("Economy Rate")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_econ)

                    # Bowling Avg
                    fig_bavg, ax = plt.subplots()
                    sns.barplot(data=bowl_compare_df, x='Player', y='Ave', palette="bone", ax=ax)
                    ax.set_title("Bowling Average")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_bavg)
                else:
                    st.warning("No bowling data for selected players.")

elif batting_stats.empty or bowling_stats.empty or fielding_stats.empty or wk_stats.empty: 
    st.error("Dataframes are empty. Failed to load or clean CSV files.")