# German Federal Election Narrative Tree App

This project presents an interactive web application for analyzing the political narratives of the 2025 German Federal Election. It allows users to explore how different political parties framed key campaign issues, cast characters in specific roles (protagonist, antagonist, etc.), and constructed their campaign stories.

## About the Application

This interactive tool deconstructs the political messaging of the 2025 German Federal Election. Instead of just looking at policies, it analyzes the **stories** each party told to persuade voters.

The application provides the following features:

* **Narrative Tree Visualization**: A hierarchical tree that visualizes how political parties frame key issues by casting different actors in specific roles.
* **Narrative Emplotment**: A breakdown of the core plot of each narrative, including the crisis, cause, conflict, and resolution.
* **Event Timeline**: A timeline of key real-world events that influenced the campaign narratives.
* **Filtering**: Users can filter the visualizations by party, theme, and narrative role to focus on specific aspects of the campaign.

## How to Run the Application

To run this application locally, you need to have Python and Streamlit installed.

1.  **Clone the repository.**
2.  **Install the required packages:**
    ```bash
    pip install streamlit pandas streamlit-timeline streamlit-agraph streamlit-scrollable-textbox
    ```
3.  **Run the Streamlit app:**
    ```bash
    streamlit run timeline_app.py
    ```

## Data Sources

The application uses the following data sources:

* `narrative_data.json`: Contains the core data for the narrative analysis, including party platforms, themes, characters, and emplotment details.
* `Events-BTW.csv`: Provides a timeline of key events relevant to the 2025 German Federal Election.

## Narrative Analysis Framework

The analysis is based on a narrative framework that examines how political campaigns create competing realities through storytelling. The key elements of this framework are:

* **Characters**: Assigning roles like "Hero," "Villain," and "Victim" to different groups to create a simple moral drama.
* **Emplotment**: Arranging events into a plot with a clear **Crisis** (the problem), **Cause** (who's to blame), **Conflict** (the battle being fought), and **Resolution** (the proposed solution).
* **Temporality**: Framing the story's timeline. Is it a sudden crisis needing urgent action, or a long-term problem requiring patience?
