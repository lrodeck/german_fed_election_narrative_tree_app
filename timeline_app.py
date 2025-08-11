# streamlit_app.py
import streamlit as st
from streamlit_timeline import timeline
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit.components.v1 as components

# Load and preprocess data
df = pd.read_csv('Events-BTW.csv')
df['Start Date'] = pd.to_datetime(df['Start Date'], format='%d/%m/%Y')
df['End Date'] = pd.to_datetime(df['End Date'], format='%d/%m/%Y')
df['Relevant Topics'] = df['Relevant Topics'].str.split(',')
df = df.explode('Relevant Topics')
df['Relevant Topics'] = df['Relevant Topics'].str.strip()

def date_to_dict(date):
    return {
        "year": date.year,
        "month": date.month,
        "day": date.day
    }

items = [
    {
        "start_date": date_to_dict(row['Start Date']),
        "end_date": date_to_dict(row['End Date']),
        "text": {
            "headline": row['Event Name'],
            "text": row['Long Text Description'] if 'Long Text Description' in row else row['Description']
        },
        "group": row['Relevant Topics']
    }
    for _, row in df.iterrows()
]

timeline_data = {
    "title": {
        "text": {
            "headline": "Event Timeline",
            "text": "Key events by relevant topic"
        }
    },
    "events": items
}


# Data object for the 2025 German Federal Election Narrative Analysis
# This data structure is designed to be used with the narrative_tree_visualization script.

# get narrrative data from narrative_data.json
import json
with open('narrative_data.json', 'r') as f:
    narrative_data = json.load(f)

# Data for the election results, extracted from the analysis document.
election_results_data = {
    'Party': ['CDU/CSU', 'AfD', 'SPD', 'Greens', 'Die Linke', 'FDP', 'BSW'],
    'Color': ['#000000', '#009EE0', '#E3000F', '#64A12D', '#BE3075', '#FFED00', '#800080'],
    'Percentage': [28.5, 20.8, 16.4, 11.6, 8.8, 4.3, 4.98],
    'Seats': [208, 152, 120, 85, 64, 0, 0]
}
results_df = pd.DataFrame(election_results_data)

# Data object for the 2025 German Federal Election Narrative Analysis
# Narrative Tree Visualization
def create_narrative_tree(data, selected_party, selected_theme, selected_role):
    """Builds and displays a filtered interactive narrative tree for characters."""
    nodes, edges = [], []
    role_colors = {"Protagonist": "#84998D", "Antagonist": "#B58D6E", "Victim": "#938BA1", "Ally/Helper": "#7D92A1", "Neutral": "#A1A1A1"}

    nodes.append(Node(id="election", label=data["election_title"], size=25, color="#FFC300"))

    for party_id, party_info in data["parties"].items():
        if selected_party == "All Parties" or party_info["label"] == selected_party:
            nodes.append(Node(id=party_id, label=party_info["label"], size=20, color=party_info["color"]))
            edges.append(Edge(source="election", target=party_id))

            if "themes" in party_info:
                for theme_id, theme_info in party_info["themes"].items():
                    if selected_theme == "All Themes" or theme_info["label"] == selected_theme:
                        theme_node_id = f"{party_id}_{theme_id}"
                        nodes.append(Node(id=theme_node_id, label=theme_info["label"], size=15, color=party_info["color"]))
                        edges.append(Edge(source=party_id, target=theme_node_id))

                        if "characters" in theme_info:
                            for character in theme_info["characters"]:
                                char_role = character.get("role", "Neutral")
                                if selected_role == "All Roles" or char_role == selected_role:
                                    char_name = character["name"]
                                    char_id = f"{theme_node_id}_{char_name.replace(' ', '_').replace('/', '_')}"
                                    char_color = role_colors.get(char_role, "#A1A1A1")
                                    char_title = f"Character: {char_name}\nRole: {char_role}"
                                    nodes.append(Node(id=char_id, label=char_name, size=10, color=char_color, title=char_title))
                                    edges.append(Edge(source=theme_node_id, target=char_id))

    config = Config(width=1200, height=850, directed=True, hierarchical={"enabled": True, "direction": "UD", "levelSeparation": 300, "nodeSpacing": 200, "treeSpacing": 250}, physics=False)
    agraph(nodes=nodes, edges=edges, config=config)


def create_emplotment_display(data, selected_party, selected_theme):
    """Zeigt die Emplotment-Daten als Markdown an."""

    # Container für die Ausgabe
    container = st.container()

    has_content = False

    for party_id, party_info in data["parties"].items():
        # Partei-Filter anwenden
        if selected_party != "All Parties" and party_info["label"] != selected_party:
            continue

        party_content = []

        for theme_id, theme_info in party_info.get("themes", {}).items():
            # Theme-Filter anwenden
            if selected_theme != "All Themes" and theme_info["label"] != selected_theme:
                continue

            emplotment = theme_info.get("emplotment")
            if isinstance(emplotment, dict) and any(emplotment.values()):
                has_content = True
                party_content.append({
                    "theme": theme_info["label"],
                    "emplotment": emplotment
                })

        # Partei-Inhalte anzeigen, falls vorhanden
        if party_content:
            with container:
                st.markdown(f"### {party_info['label']}")

                for content in party_content:
                    st.markdown(f"**{content['theme']}**")
                    st.markdown(f"**Events Included:** {content['emplotment'].get('Events Included', 'N/A')}")
                    st.markdown(f"**Events Excluded:** {content['emplotment'].get('Events Excluded', 'N/A')}")
                    st.markdown(f"**Sequence and Temporality:** {content['emplotment'].get('Sequence and Temporality', 'N/A')}")
                    st.markdown(f"**Crisis:** {content['emplotment'].get('Crisis', 'N/A')}")
                    st.markdown(f"**Cause:** {content['emplotment'].get('Cause', 'N/A')}")
                    st.markdown(f"**Conflict:** {content['emplotment'].get('Conflict', 'N/A')}")
                    st.markdown(f"**Resolution:** {content['emplotment'].get('Resolution', 'N/A')}")
                    st.markdown("---")

    if not has_content:
        st.info("Keine Emplotment-Daten für die aktuelle Filterauswahl.")




# --- STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Narrative Analysis Dashboard", layout="wide")
# Inject CSS for the scrollable container
st.markdown("""
<style>
.scrollable-container {
    height: 850px; /* Match the height of the graph */
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #e6e6e6;
    border-radius: 10px;
}
.emplotment-item {
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e6e6e6;
}
.emplotment-item p {
    margin-bottom: 0.25rem; /* Tighter spacing between lines */
    font-size: 0.9rem;
}
.theme-title {
    margin-bottom: 0.5rem;
}
h4 {
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)
st.title("🇩🇪 2025 German Election: A Narrative Analysis")
st.markdown("""This interactive tool deconstructs the political messaging of the 2025 German Federal Election. Instead of just looking at policies, it analyzes the **stories** each party told to persuade voters.\n
Select a party and a key campaign issue from the sidebar to see how they framed their reality, who they cast as the heroes and villains, and what future they promised.""")
# --- ELECTION RESULTS AND CONTEXT ---

st.header("The Electoral Earthquake: Results and Repercussions")
st.markdown("""
The German federal election on February 23, 2025, produced a political earthquake, fundamentally altering the balance of power in the Bundestag (Crisis, Conflict, and Realignment, 2025). The results delivered a decisive victory for the conservative CDU/CSU, a historic surge for the far-right Alternative für Deutschland (AfD), and a catastrophic collapse for the governing parties, particularly the Social Democratic Party (SPD) (Crisis, Conflict, and Realignment, 2025).
""")


col_results1, col_results2 = st.columns([1, 1.5])

with col_results1:
    st.dataframe(results_df.style.apply(lambda x: [f'background-color: {x.Color}; color: {"white" if x.Color in ["#000000", "#BE3075", "#800080", "#E3000F"] else "black"}' for i in x], axis=1), hide_index=True)

with col_results2:
    st.bar_chart(results_df, x="Party", y="Percentage", color="Color")

st.info("""
**A Key Consequence: The Blocking Minority**

The new "Grand Coalition" of the CDU/CSU and SPD holds 328 of the 630 seats in the Bundestag (Crisis, Conflict, and Realignment, 2025). However, constitutional amendments in Germany require a two-thirds supermajority, which amounts to 420 seats (Crisis, Conflict, and Realignment, 2025). The combined strength of the two primary opposition parties, the **AfD (152 seats)** and **Die Linke (64 seats)**, totals 216 seats. This is well over the one-third of seats needed to form a "blocking minority" (Crisis, Conflict, and Realignment, 2025). This dynamic means that resolving contentious constitutional issues, such as reforming the national debt brake, is now structurally impossible for the new government without securing support from parties on the political fringe (Crisis, Conflict, and Realignment, 2025).
""", icon="🏛️")

st.markdown("---")

st.markdown("""### What is Narrative Analysis?

Political campaigns are battles of competing realities. **Narrative Analysis** is a method used to understand how parties create these realities through storytelling. It reveals that political debates are often not just about facts and policies, but about which story voters find most believable and compelling.

Every political narrative contains a few key elements:  

* **🎭 Characters**: Assigning roles like "Hero," "Villain," and "Victim" to different groups to create a simple moral drama.  
* **📖 Emplotment**: Arranging events into a plot with a clear **Crisis** (the problem), **Cause** (who's to blame), **Conflict** (the battle being fought), and **Resolution** (the proposed solution).  
* **⏳ Temporality**: Framing the story's timeline. Is it a sudden crisis needing urgent action, or a long-term problem requiring patience?  

This framework helps decode the persuasive strategies at the heart of political communication.""")

# --- Sidebar ---
st.sidebar.markdown("### Instructions")
st.sidebar.write("Use the filters below to explore the narrative structures and related events.")

party_list = ["All Parties"] + [p["label"] for p in narrative_data["parties"].values()]
selected_party = st.sidebar.selectbox("Filter by Party", party_list, help="Select a party to view their narrative structure.")

theme_list = ["All Themes"] + sorted(list(set(t["label"] for p in narrative_data["parties"].values() for t in p.get("themes", {}).values())))
selected_theme = st.sidebar.selectbox("Filter by Theme", theme_list, help="Focus on a specific thematic battleground.")

role_list = ["All Roles", "Protagonist", "Antagonist", "Victim", "Ally/Helper", "Neutral"]
selected_role = st.sidebar.selectbox("Filter by Narrative Role", role_list, help="Isolate characters by their narrative role in the tree.")

st.sidebar.markdown("### Role Legend")
role_colors = {"Protagonist": "#84998D", "Antagonist": "#B58D6E", "Victim": "#938BA1", "Ally/Helper": "#7D92A1", "Neutral": "#A1A1A1"}
for role, color in role_colors.items():
    st.sidebar.markdown(f"<div style='display: flex; align-items: center; margin-bottom: 5px;'><div style='width: 15px; height: 15px; background-color: {color}; border-radius: 50%; margin-right: 10px;'></div>{role}</div>", unsafe_allow_html=True)



st.header("Related Event Timeline")
st.write("This timeline shows key real-world events that influenced the campaign narratives. It filters along with the tree visualization.")
timeline(timeline_data, height=600)




# --- Main Content Area (Two Columns) ---
col1, col2 = st.columns([2, 1]) # Tree gets 2/3 of the space, auxiliary visuals get 1/3

with col1:
    st.header("Narrative Tree Visualization")
    st.write("This tree visualizes how political parties frame key issues by casting different actors in specific roles. Use the filters to explore.")
    create_narrative_tree(narrative_data, selected_party, selected_theme, selected_role)

with col2:
    st.header("Narrative Emplotment")
    st.write("This section breaks down the core plot of each narrative (Crisis, Cause, Conflict, Resolution).")
    with st.container(border=True, height=850):
        create_emplotment_display(narrative_data, selected_party, selected_theme)

