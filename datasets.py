import streamlit as st
import pandas as pd

DATASET_METADATA = {
    "gk": {
        "name": "Garis Kemiskinan Per Kapita", 
        "description": "Garis Kemiskinan Per Kapita dengan disagregasi Provinsi, Tahun, Periode Survei, Jenis Pengeluaran, dan Daerah Tempat Tinggal.",
        "path": "./dataset_kesejahteraan_pekerja_indonesia/gk.df.csv",
    },
    "peng": {
        "name": "Pengeluaran Per Kapita", 
        "description": "Rata-Rata Pengeluaran Per Kapita dengan disagregasi Provinsi, Tahun, Jenis Pengeluaran, dan Daerah Tempat Tinggal.",
        "path": "./dataset_kesejahteraan_pekerja_indonesia/peng.df.csv",
    },
    "ump": {
        "name": "Upah Minimum Provinsi",
        "description": "Upah Minimum Provinsi (UMP) dengan disagregasi Provinsi dan Tahun.",
        "path": "./dataset_kesejahteraan_pekerja_indonesia/ump.df.csv",
    },
    "upah": {
        "name": "Rata-Rata Upah Pekerja Per Jam",
        "description": "Rata-Rata Upah Pekerja Per Jam dengan disagregasi Provinsi dan Tahun.",
        "path": "./dataset_kesejahteraan_pekerja_indonesia/upah.df.csv",
    },
}

@st.cache_data
def load_datasets():
    datasets = {}
    for key, value in DATASET_METADATA.items():
        df = pd.read_csv(value["path"])
        datasets[key] = df
        datasets["name"] = value["name"]
        datasets["description"] = value["description"]
    return datasets

def get_dataset_metadata():
    return DATASET_METADATA