import time
import streamlit as st
import pandas as pd
import backend.demand as demand
import backend.agent as agent
import backend.demand_type as demand_type
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
    
    st.title("Agent-Based Simulation for Cloud Strategies")

    st.header("Workloads")
    name = st.text_input("Name")
    workload_type = st.segmented_control(
        "Workload Type", [dt.name.replace("_"," ") for dt in demand_type.DemandType], selection_mode="single"
    )
    start_time = st.number_input("Start Time (sec)", step=1, min_value=0)
    num_of_instances = st.number_input("Number of Instances", step=1, min_value=1)
    repeat_every = st.number_input("Repeat Every (sec)", step=1, min_value=0)
    repeat_until = st.number_input("Repeat Until (sec)", step=1, min_value=0)
    duration = st.number_input("Duration (sec)", step=1, min_value=1)
    memory_gib =  st.number_input("Memory (GiB)", step=1, min_value=1)
    vcpus = st.number_input("vCPUs", step=2, min_value=2)

    if st.button("Add Workload!"):
        new_demand = demand.Demand(
            name=name,
            workload_type=workload_type,
            start_time=start_time,
            num_of_instances=num_of_instances,
            repeat_every=repeat_every,
            repeat_until=repeat_until,
            duration=duration,
            memory_gib=memory_gib,
            vcpus=vcpus
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

    st.header("Compute Resources")
    resource_name = st.text_input("Resource Name")
    cluster_hardware_type = st.segmented_control(
        "Cluster Hardware Type", ["demand.HARDWARE_TYPES"], selection_mode="single", key="cluster_hardware_type"
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
    
    st.header("Agents (Teams)")
    eng_team_name = st.text_input("Team Name")
    team_scope = st.segmented_control(
        "Team Scope", ["AI R&D", "AI Production", "Apps", "Internal IT"], selection_mode="single", key="eng_team_scope"
    )
    
    if st.button("Add Team!"):
        pass

    st.header("Strategy")
    strategy = st.segmented_control(
        "Strategy", ["Cost Cutting", "AI First", "Apps First", "Bottom Up"], selection_mode="single", key="strategy"
    )
    
    if st.button("Add Strategy!"):
        pass
    
    st.header("Run Simulation")  
    st.button("Run!")

if __name__ == "__main__":
    main()