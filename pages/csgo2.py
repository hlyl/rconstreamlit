import streamlit as st
import configparser
from rcon.source import Client
import json
import re


# Your existing functions
def run_rcon_command(command, *args):
    config = configparser.ConfigParser()
    config.read("config.ini")

    ip = config["RCON"]["ip"]
    port = int(config["RCON"]["port"])
    password = config["RCON"]["password"]
    with Client(ip, port, passwd=password) as client:
        # Convert all arguments to strings
        str_args = [str(arg) for arg in args]
        response = client.run(command, *str_args)
    return response


# Streamlit app
def main():
    st.title("Counterstrike2")
    response = run_rcon_command("status")
    # Regular expression pattern to find player names
    pattern = r"'\w+'"

    # Find all matches
    matches = re.findall(pattern, response)

    # Extract player names from matches
    player_names = [match.strip("'") for match in matches]

    print(player_names)
    st.text(f"Players: {player_names}")

    col1, col2, col3 = st.columns(3)
    with col1:
        # Dropdown for map selection
        map_name = st.selectbox(
            "Select a map:",
            [
                "de_dust2",
                "de_mirage",
                "de_inferno",
                "de_overpass",
                "de_nuke",
                "de_train",
                "de_vertigo",
            ],
        )

    with col2:
        # Button for execution
        if st.button("Change Map"):
            response = run_rcon_command("changelevel", map_name)
            st.success(f"Response: {response}")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Create a button to remove bots
        if st.button("Remove Bots"):
            response = run_rcon_command("bot_kick")
            st.success(f"Response: {response}")

    with col2:
        # Create a button to add bots to ct
        if st.button("Add CT Bots"):
            response = run_rcon_command("bot_add_ct expert")
            st.success(f"Response: {response}")

    with col3:
        # Create a button to add bots to t
        if st.button("Add T Bots"):
            response = run_rcon_command("bot_add_t expert")
            st.success(f"Response: {response}")


if __name__ == "__main__":
    main()
