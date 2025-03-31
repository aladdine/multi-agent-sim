import time
import streamlit as st
import pandas as pd
from backend import demand
import numpy as np

if 'demand_table' not in st.session_state:
    demand_table = demand.DemandTable()
    st.session_state['demand_table'] = demand_table
else:
    demand_table = st.session_state['demand_table']

def main():
    
    st.title("Agent-Based Simulation for Data Center Strategies")

    st.header("Demand")
    name = st.text_input("Name")
    hardware_type = st.segmented_control(
        "Hardware Type", demand.HARDWARE_TYPES, selection_mode="single"
    )
    start_time = st.number_input("Start Time (sec)", step=1, min_value=1)
    delayable = st.checkbox("Delayable")
    num_of_jobs = st.number_input("Number of Jobs", step=1, min_value=1)
    repeat_every = st.number_input("Repeat Every (sec)", step=1, min_value=0)
    duration = st.number_input("Duration (sec)", step=1, min_value=1)
    power_consumption = st.number_input("Power Consumption (W)", step=1, min_value=0)
    heat_decipation = st.number_input("Heat Decipation (W)", step=1, min_value=0)


    if st.button("Add Demand!"):
        new_demand = demand.Demand(
            name=name,
            hardware_type=hardware_type,
            start_time=start_time,
            delayable=delayable,
            num_jobs=num_of_jobs,
            repeat_every=repeat_every,
            duration=duration,
            power_consumption=power_consumption,
            heat_decipation=heat_decipation
        )
        print("called")
        demand_table.add_demand(new_demand)
    
        demand_added = st.success('Demand added!', icon="✅")
        time.sleep(1)
        demand_added.empty()
    
        table = st.table(
            demand_table.get_df()
        )
    
    
    chart = st.bar_chart()


if __name__ == "__main__":
    main()