import time
import streamlit as st
import pandas as pd
from backend import demand, agent
import numpy as np



if 'demand_table' not in st.session_state:
    demand_table = demand.DemandTable()
    st.session_state['demand_table'] = demand_table
else:
    demand_table = st.session_state['demand_table']

if 'cluster_table' not in st.session_state:
    cluster_table = agent.ClusterTable()
    st.session_state['cluster_table'] = cluster_table
else:
    cluster_table = st.session_state['cluster_table']

def main():
    
    st.title("Agent-Based Simulation for Data Center Strategies")

    st.header("Workloads")
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


    if st.button("Add Workload!"):
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

        demand_table.add_demand(new_demand)
    
        demand_added = st.success('Demand added!', icon="✅")
        time.sleep(1)
        demand_added.empty()
        chart_data = demand_table.get_chart()
        workload_bar_chart = st.bar_chart(chart_data)
        workload_table = st.table(
            demand_table.get_df()
        )

    st.header("Clusters")
    cluster_name = st.text_input("Cluster Name")
    cluster_hardware_type = st.segmented_control(
        "Cluster Hardware Type", demand.HARDWARE_TYPES, selection_mode="single", key="cluster_hardware_type"
    )
    cluster_size = st.number_input("Cluster Size (# of servers)", min_value=1, step=1)
    failure_rate = st.number_input("Failure Rate")
    if st.button("Add Cluster!"):
        new_cluster = agent.Cluster(
            name=cluster_name,
            hardware_type=cluster_hardware_type,
            size=cluster_size,
            failure_rate=failure_rate
        )

         
        cluster_table.add_cluster(new_cluster)
        
    
        cluster_added = st.success('Cluster added!', icon="✅")
        time.sleep(1)
        cluster_added.empty()
        all_clusters_table = st.table(
            cluster_table.get_df()
        )
    
    st.header("Run Simulation")
    scheduling_algorithm = st.segmented_control(
        "Scheduling Algorithm", ["FIFO (throughput)", "Power Efficient (Power Capping)", "Power Efficient (Load Stacking)"], selection_mode="single", key="scheduling_algorithm"
    )  
    st.button("Run!")

if __name__ == "__main__":
    main()